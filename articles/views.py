from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Article
from .forms import ArticleForm
 
def articles(request):
    """ View to display all articles """
    all_articles = Article.objects.filter(is_deleted=False).order_by('-posted_date')
    template = 'articles/articles.html'
    context = {
        'articles': all_articles,
    }
    
    return render(request, template, context)

    
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
