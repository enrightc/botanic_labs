from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Season


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput(attrs={
            'class': 'new-image border-black rounded-0'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        seasons = Season.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in seasons]

        self.fields['season'].choices = friendly_names
        for field_name, field in self.fields.items():
            # Skip image field as its already set its class
            if field_name != 'image':
                field.widget.attrs['class'] = 'border-black rounded-0'
