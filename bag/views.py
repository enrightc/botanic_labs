from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    '''
    A view to return the bag contents page
    '''
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # check the user’s session to see if there’s already a shopping bag stored.
    bag = request.session.get('bag', {})

    # Check if the product (item_id) is already in the shopping bag.
    if item_id in list(bag.keys()):
        # If the product is already in the bag increment the quantity of that product 
        bag[item_id] += quantity
        request.session['show_bag_summary'] = True  # Ensure bag summary is shown when adding to bag
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        # If the product is not in the bag add it with the specified quantity
        bag[item_id] = quantity
        # Display success message to the user
        messages.success(request, f'Added {product.name} to your bag')

    # Save the shopping bag into the user's session
    request.session['bag'] = bag
    

    # Print the value of show_bag_summary to the terminal for debugging
    print(request.session.get('show_bag_summary'))

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust quantuty of an item to a specfied amount """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        # Update the quantity of the item in the bag
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        # Remove the item from the bag if quantity is 0 or less
        bag.pop(item_id)
        messages.success(request, f'Removed {product.name} from your bag')


    # Save the updated bag back to the session
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})

        # Remove the item from the bag
        if item_id in bag:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your bag')

        # Save the updated bag back to the session
        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: (e)')
        return HttpResponse(status=500)