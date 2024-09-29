from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm
 
def articles(request):
    """ View to display all articles """
    
    articles = Article.objects.filter(status=1).order_by('-posted_date')
    
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

    
@login_required # Django will check whether the user is logged in before executing the view.
def add_article(request):
    """ View to create a new article """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False) # Create article instance but don't save to DB yet
            article.author = request.user # Set the author
            article.save()  # Now save the article with the author set
            messages.success(request, 'Successfully added article!')
            return redirect(reverse('articles'))
        else:
            messages.error(request, 'Failed to add article. Please ensure the form is valid.')
    else:
        form = ArticleForm()
        
    template = 'articles/add_article.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
