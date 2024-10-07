from django import forms
from .models import Faq
from django_summernote.widgets import SummernoteWidget


class FaqForm(forms.ModelForm):
    """
    Form to create a new FAQ
    """

    class Meta:
        model = Faq
        fields = [
            'question',  'answer',
        ]

        widgets = {
            'answer': SummernoteWidget(),
            'question': forms.Textarea(attrs={'rows': 3}),
        }

        labels = {
            "question": "question",
            "answer": "Answer"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
