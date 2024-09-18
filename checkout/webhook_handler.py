from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from bag.contexts import bag_contents

import stripe
import json


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    # This method is automatically called when an instance of the class is created
    # It takes the request as an argument and stores it in the instance
    def __init__(self, request):
        self.request = request

     # This method handles generic, unknown, or unexpected webhook events from Stripe
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',  # Sends a response indicating an unhandled event
            status=200)  # Status 200 means the request was successfully received and processed

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object  # The payment information sent by Stripe
        pid = intent.id  # Payment ID from Stripe
        bag = intent.metadata.bag  # The shopping bag data from Stripe's metadata
        save_info = intent.metadata.save_info  # Whether the user wants to save info for future purchases

        # Retrieve additional charge details from Stripe
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge  # Retrieves the latest charge from the payment intent
        )

        # Extract billing and shipping details
        billing_details = stripe_charge.billing_details  # Customer's billing details
        shipping_details = intent.shipping  # Customer's shipping details
        grand_total = round(stripe_charge.amount / 100, 2)  # Convert amount to the correct decimal format


        # Clean up the shipping address data (replace empty fields with None)
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        order_exists = False  # This flag tracks if the order is already in the database
        attempt = 1  # Start a loop to try checking for the order multiple times
        while attempt <= 5: # Retry up to five times in case view is delayed and hasnt created the order by the time we get the webhook from stripe. 
            try:
                # Try to find an existing order that matches the payment and shipping details
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
                    grand_total=grand_total,  # Ensure the grand total matches the one from Stripe
                    original_bag=bag,  # Check if the bag details match
                    stripe_pid=pid,  # Check if the Stripe Payment ID matches
                )
                order_exists = True  # If the order is found, mark it as existing
                break  # Stop trying once the order is found
            except Order.DoesNotExist:  # If the order doesn't exist, try again after a short delay
                attempt += 1
                time.sleep(1)  # Wait for 1 second before trying again
        
        if order_exists:
        # If the order exists, return a success message
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            # If the order doesn't exist, create a new one
            order = None
            try:
                order = Order.objects.create(
                    full_name=shipping_details.name,
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
                        product = Product.objects.get(id=item_id)  # Get the product from the database
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
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)


    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)