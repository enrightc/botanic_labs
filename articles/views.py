from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm


def articles(request):
    """ View to display all articles """

    articles = Article.objects.filter(
        status=1, is_deleted=False).order_by('-posted_date')

    context = {
        'articles': articles,
    }

    return render(request, 'articles/articles.html', context)


def article(request, slug):
    """ View to display an article """

    article = get_object_or_404(Article, slug=slug)
    context = {
        'article': article,
    }

    return render(request, 'articles/article.html', context)


def admin_articles_view(request):
    """ View to allow admin to manage articles """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))

    if request.user.is_superuser:
    
        articles = Article.objects.all()
        context = {
            'articles': articles,
        }

        return render(request, 'articles/admin_articles_view.html', context)

    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))


# Django will check whether the user is logged in before executing the view.
def add_article(request):
    """ View to create a new article """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))

    if request.user.is_superuser:
        
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                # Create article instance but don't save to DB yet
                article = form.save(commit=False)
                # Set the author
                article.author = request.user
                article.save()  # Now save the article with the author set
                # disable bag summary
                request.session['show_bag_summary'] = False
                messages.success(request, 'Successfully added article!')
                return redirect(reverse('admin_articles_view'))
            else:
                messages.error(
                    request,
                    'Failed to add article. Please ensure the form is valid.'
                )
        else:
            form = ArticleForm()

        template = 'articles/add_article.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
    
    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))


def edit_article(request, slug):
    """
    View to allow admin to edit an article
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))

    if request.user.is_superuser:
        
        # Get the article object by its slug or return a 404 error if not found
        article = get_object_or_404(Article, slug=slug)

        # Check if the request is a POST (form submission)
        if request.method == 'POST':
            # Create a form instance with the POST data and any uploaded files
            # 'instance=article' means form will be
            # pre-populated with the article data
            form = ArticleForm(request.POST, request.FILES, instance=article)

            # Validate the form data
            if form.is_valid():
                # If the form is valid,
                # save the updated product information to the database
                form.save()
                request.session['show_bag_summary'] = False
                # Display a success message to the user
                messages.success(request, 'Successfully updated article!')
                return redirect(reverse('article', args=[article.slug]))
            else:
                # If the form is not valid, show an error message
                messages.error(
                    request,
                    'Failed to update article. Please ensure the form is valid.')

        # If the request method is not POST,
        # show the form with the current product data for editing
        else:
            # Pre-populate the form with the articles current information
            form = ArticleForm(instance=article)
            # Display a message to inform the user which product is being edited
            messages.info(request, f'You are editing {article.title}')

        # Set the template to use for rendering the form
        template = 'articles/edit_article.html'

        # Prepare the context with the form and product to send to the template
        context = {
            'form': form,
            'article': article,
        }

        # Render the edit product template with the context data
        return render(request, template, context)

    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))


def delete_article(request, slug):
    """ Delete a article from the store """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))

    if request.user.is_superuser:
        
        article = get_object_or_404(Article, slug=slug)
        article.delete()
        request.session['show_bag_summary'] = False
        messages.success(request, 'Article deleted!')
        return redirect(reverse('admin_articles_view'))
    
    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
