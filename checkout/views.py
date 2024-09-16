from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Po09mP0uuJh6VgEt4P1qYzxH4hjcXi5Ptcw5M3lcLJISvP4gol8oG7oHQnL1sJnjEx9IoeSqaU6y3nJXt1iuh5v00AbNcNUJM',
        'client_secret': 'test client secret'
    }

    return render(request, template, context)