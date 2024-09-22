from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower

from .forms import ProductForm
from .models import Product, Season

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    seasons = None
    sort = None
    direction = None

    # Always fetch all seasons for navigation
    all_seasons = Season.objects.all()

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'season' in request.GET:
                seasons = request.GET['season'].split(',')
                products = products.filter(season__name__in=seasons)
                current_seasons = Season.objects.filter(name__in=seasons)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_seasons': seasons,
        'all_seasons': all_seasons,  # All seasons for navigation
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    '''
    A view to show individual product details
    '''

    product = get_object_or_404(Product, pk=product_id) # get only one product using the product id.

    # Get the recommended products if they exist
    recommended_products = []
    if product.recommendation_1:
        recommended_products.append(product.recommendation_1)
    if product.recommendation_2:
        recommended_products.append(product.recommendation_2)
    if product.recommendation_3:
        recommended_products.append(product.recommendation_3)

    context = {
        'product': product,
        'recommended_products': recommended_products,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)