from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm, NameForm
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    user = request.user

    if request.method == 'POST':
        # Pass submitted data to both forms
        delivery_form = UserProfileForm(request.POST, instance=profile)
        name_form = NameForm(request.POST, instance=user)

        # Check both forms for validity
        if delivery_form.is_valid() and name_form.is_valid():
            # Save both forms to update the user's profile and name
            delivery_form.save()
            name_form.save()
            request.session['show_bag_summary'] = False  # disable bag summary
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request, 'Update failed. Please ensure the form is valid.'
            )
    else:
        # Populate the forms with existing user and profile data
        delivery_form = UserProfileForm(instance=profile)
        name_form = NameForm(instance=user)

    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'delivery_form': delivery_form,
        'name_form': name_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
