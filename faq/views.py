from django.shortcuts import (
    render, redirect,
    reverse, get_object_or_404
)
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


# Django will check whether the user is logged in before executing the view.
def add_faq(request):
    """ View to create a new faq """
    if not request.user.is_authenticated:
            messages.error(request, 'Please log in to access this feature.')
            return redirect(reverse('account_login'))

    if request.user.is_superuser:
        
        if request.method == 'POST':
            form = FaqForm(request.POST, request.FILES)
            if form.is_valid():
                # Create faq instance but don't save to DB yet
                faq = form.save(commit=False)
                faq.save()  # Now save the faq form
                request.session['add_to_bag'] = False  # Disable the bag summary
                request.session['show_bag_summary'] = False
                messages.success(request, 'Successfully added FAQ!')
                return redirect(reverse('faq'))
            else:
                messages.error(
                    request, 'Failed to add FAQ. Please ensure the form is valid.'
                )
        else:
            form = FaqForm()

        template = 'faq/add_faq.html'
        context = {
            'form': form,
            # Pass to template
            'show_bag_summary': request.session.get('show_bag_summary', True)
        }

        return render(request, template, context)

    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))


# Django will check whether the user is logged in before executing the view.
def delete_faq(request, id):
    """ Delete a FAQ """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))

    if request.user.is_superuser:
        
        faq = get_object_or_404(Faq, id=id)
        faq.delete()
        request.session['show_bag_summary'] = False
        messages.success(request, 'FAQ deleted!')
        return redirect(reverse('faq'))

    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))


def edit_faq(request, id):
    """
    View to allow admin to edit an FAQ
    """
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to access this feature.')
        return redirect(reverse('account_login'))
        
    if request.user.is_superuser:
        
        faq = get_object_or_404(Faq, id=id)

        if request.method == 'POST':
            form = FaqForm(request.POST, request.FILES, instance=faq)

            if form.is_valid():
                form.save()
                request.session['show_bag_summary'] = False  # disable bag summary
                messages.success(request, 'FAQ updated!')
                return redirect(reverse('faq'))
            else:
                messages.error(
                    request,
                    'Failed to update faq. '
                    'Please ensure the form is valid.'
                )

        else:
            form = FaqForm(instance=faq)
            messages.info(request, f'You are editing "{faq.question}"')

        # Set the template to use for rendering the form
        template = 'faq/edit_faq.html'

        # Prepare the context with the form and product to send to the template
        context = {
            'form': form,
            'faq': faq,
        }

        # Render the edit product template with the context data
        return render(request, template, context)

    else:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
