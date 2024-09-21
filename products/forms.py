from django import forms
from .models import Product, Season


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        seasons = Season.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in seasons]

        self.fields['season'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'