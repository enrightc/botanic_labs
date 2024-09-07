from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def all_products(request):
    '''
    A view to show all products, including sorting and search queries
    '''

    products = Product.objects.all() # Get all of the products

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    '''
    A view to show individual product details
    '''

    product = get_object_or_404(Product, pk=product_id) # get only one product using the product id.

    # Get the recommended products by IDs
    recommended_ids = product.recommendations.split(",")  # Convert the string to a list
    recommended_products = Product.objects.filter(id__in=recommended_ids)  # Get the recommended products

    context = {
        'product': product,
        'recommended_products': recommended_products,
    }

    return render(request, 'products/product_detail.html', context)