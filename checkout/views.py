from django.shortcuts import (
    render, redirect, reverse,
    get_object_or_404, HttpResponse
)
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem

from products.models import Product
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from bag.contexts import bag_contents

import stripe  # Stripe is used for handling payments
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    # Get Stripe keys from settings
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Check if the request is a POST, meaning the user submitted the form
    if request.method == 'POST':
        # Get the shopping bag items from the session
        bag = request.session.get('bag', {})

        # Collect the form data from the user's POST request
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        # Create a new order form with the form data
        order_form = OrderForm(form_data)

        # Check if the form is valid (no errors in the data)
        if order_form.is_valid():
            # Save the order to the database
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
            order.save()
            # Loop through each item in the shopping bag
            for item_id, item_data in bag.items():
                try:
                    # Try to get the product from the database using its ID
                    product = Product.objects.get(id=item_id)

                    # Create an order line item (a single product in the order)
                    order_line_item = OrderLineItem(
                        order=order,  # Connect this line item to the order
                        product=product,  # Specify which product it is
                        # Specify the quantity of the product
                        quantity=item_data,
                    )
                    # Save the line item to the database
                    order_line_item.save()

                # If the product is not found in the database
                except Product.DoesNotExist:
                    # Show an error message to the user
                    messages.error(
                        request,
                        (
                            "One of the products in your bag wasn't found "
                            "in our database. Please call us for assistance!"
                        )
                    )
                    # Delete the order
                    # since it cannot be completed without the product
                    order.delete()
                    # Redirect the user back to their shopping bag
                    return redirect(reverse('view_bag'))

            # Save user's preference to save their info if they checked the box
            request.session['save_info'] = 'save-info' in request.POST

            # Redirect to the checkout success page with the order number
            return redirect(
                reverse(
                    'checkout_success', args=[order.order_number]
                )
            )
        else:
            # If the form is invalid, show an error message to the user
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    # If the user is just viewing the checkout page and
    # hasn't submitted the form yet
    bag = request.session.get('bag', {})

    # If the bag is empty, show an error and redirect to the products page
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    else:
        # Get the current bag contents and calculate the totals
        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)  # Stripe expects amount in pennies
        stripe.api_key = stripe_secret_key  # Set the secret key for Stripe

        # Create a payment intent for Stripe (used to process the payment)
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,  # Amount to be charged
            currency=settings.STRIPE_CURRENCY,  # Currency type
        )

        # Attempt to prefill the form with any info the user profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            # Create an empty order form for the user to fill out
            order_form = OrderForm()

        # If Stripe public key is missing, warn the user
        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        # Set the template to be used and pass context (data) to the template
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,  # The form the user will fill out
            # Stripe key for the frontend
            'stripe_public_key': stripe_public_key,
            # Secret key for Stripe payment intent
            'client_secret': intent.client_secret,
        }

        # Render the checkout page with the given template and context
        return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
