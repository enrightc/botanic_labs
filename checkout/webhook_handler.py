from django.shortcuts import (
    HttpResponse
)

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile

import time
import stripe
import json


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    # method is automatically called when an instance of the class is created
    # It takes the request as an argument and stores it in the instance
    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'confirmation_emails/confirmation_email_subject.txt',
            {'order': order}).strip()
        body = render_to_string(
            'confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    # This method handles generic, unknown,
    # or unexpected webhook events from Stripe
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            # Sends a response indicating an unhandled event
            content=f'Unhandled webhook received: {event["type"]}',
            # Status 200 = the request was successfully received and processed
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object  # The payment information sent by Stripe
        pid = intent.id  # Payment ID from Stripe
        # The shopping bag data from Stripe's metadata
        bag = intent.metadata.bag
        # Whether the user wants to save info for future purchases
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        # Extract billing and shipping details
        # Customer's billing details
        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping  # Customer's shipping details
        # Convert amount to the correct decimal format
        grand_total = round(stripe_charge.amount / 100, 2)

        # Clean up the shipping address data (replace empty fields with None)
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        # Update profile information if save_info was checked
        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_phone_number = shipping_details.phone
                profile.default_country = shipping_details.address.country
                profile.default_postcode = shipping_details.address.postal_code
                profile.default_town_or_city = shipping_details.address.city
                profile.default_street_address1 = (
                    shipping_details.address.line1
                )
                profile.default_street_address2 = (
                    shipping_details.address.line2
                )
                profile.default_county = shipping_details.address.state
                profile.save()

        # This flag tracks if the order is already in the database
        order_exists = False
        # Start a loop to try checking for the order multiple times
        attempt = 1
        # Retry up to five times in case view is delayed and hasnt created
        # the order by the time we get the webhook from stripe.
        while attempt <= 5:
            try:
                # Try to find an existing order that matches
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    # Ensure the grand total matches the one from Stripe
                    grand_total=grand_total,
                    original_bag=bag,  # Check if the bag details match
                    stripe_pid=pid,  # Check if the Stripe Payment ID matches
                )
                # If the order is found, mark it as existing
                order_exists = True
                break  # Stop trying once the order is found
            # If the order doesn't exist, try again after a short delay
            except Order.DoesNotExist:
                attempt += 1
                time.sleep(1)  # Wait for 1 second before trying again

        if order_exists:
            # If order exists send confirmation email before
            # returning response to stripe
            self._send_confirmation_email(order)
        # If the order exists, return a success message
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    'SUCCESS: Verified order already in database'
                ),
                status=200)
        else:
            # If the order doesn't exist, create a new one
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # Iterate over each item in the bag and add it to the order
                for item_id, item_data in json.loads(bag).items():
                    # Get the product from the database
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()  # Save the order line item

            except Exception as e:
                # If something goes wrong, delete the order and return an error
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                'SUCCESS: Created order in webhook'
            ),
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
