from django.shortcuts import render, get_object_or_404
#from django.contrib import messages
#from django.contrib.auth.decorators import login_required

from .models import Faq

 
def faqs(request):
    """ View to display all faqs """
    
    faqs = Faq.objects.filter()
    
    context = {
        'faqs': faqs,
    }
    
    return render(request, 'faq/faq.html', context)
