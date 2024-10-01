from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Faq
from .forms import FaqForm
 
 
def faqs(request):
    """ View to display all faqs """
    
    faqs = Faq.objects.filter()
    
    context = {
        'faqs': faqs,
    }
    
    return render(request, 'faq/faq.html', context)


@login_required # Django will check whether the user is logged in before executing the view.
def add_faq(request):
    """ View to create a new faq """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = FaqForm(request.POST, request.FILES)
        if form.is_valid():
            faq = form.save(commit=False) # Create faq instance but don't save to DB yet
            faq.save()  # Now save the faq form
            messages.success(request, 'Successfully added FAQ!')
            return redirect(reverse('faq'))
        else:
            messages.error(request, 'Failed to add FAQ. Please ensure the form is valid.')
    else:
        form = FaqForm()
        
    template = 'faq/add_faq.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

