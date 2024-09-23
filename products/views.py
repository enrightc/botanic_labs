from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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


@login_required # Django will check whether the user is logged in before executing the view.
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required # Django will check whether the user is logged in before executing the view.
def edit_product(request, product_id):
    """ 
    Edit a product in the store 
    - This view allows users to edit an existing product's details.
    - It checks if the form was submitted via POST or just loaded.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    # Get the product object by its id or return a 404 error if not found
    product = get_object_or_404(Product, pk=product_id)

    # Check if the request is a POST (form submission)
    if request.method == 'POST':
        # Create a form instance with the POST data and any uploaded files
        # 'instance=product' means the form will be pre-populated with the current product data
        form = ProductForm(request.POST, request.FILES, instance=product)

        # Validate the form data
        if form.is_valid():
            # If the form is valid, save the updated product information to the database
            form.save()
            # Display a success message to the user
            messages.success(request, 'Successfully updated product!')
            # Redirect the user to the product detail page after successful edit
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # If the form is not valid, show an error message
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')

    # If the request method is not POST, show the form with the current product data for editing
    else:
        # Pre-populate the form with the product's current information
        form = ProductForm(instance=product)
        # Display a message to inform the user which product is being edited
        messages.info(request, f'You are editing {product.name}')

    # Set the template to use for rendering the form
    template = 'products/edit_product.html'

    # Prepare the context with the form and product to send to the template
    context = {
        'form': form,
        'product': product,
    }

    # Render the edit product template with the context data
    return render(request, template, context)


@login_required # Django will check whether the user is logged in before executing the view.
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
        
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))