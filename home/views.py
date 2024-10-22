from django.shortcuts import render

# Create your views here.


def index(request):
    '''
    A view to return the index page
    '''
    return render(request, 'home/index.html')


def error_404_view(request, exception):
    """
    404 error
    """
    return render(request, 'home/404.html')


def error_500_view(request):
    """
    500 error
    """
    return render(request, 'home/500.html')
