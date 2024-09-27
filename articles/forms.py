from django import forms
from .models import Article
from django_ckeditor_5.widgets import CKEditor5Widget


class ArticleForm(forms.ModelForm):
    """
    Form to create a new article
    """
    
    class Meta:
        model = Article
        fields = [
            'title',  'content', 'excerpt', 'image', 'image_alt', 'status'
        ]

        widgets = {
            'content': CKEditor5Widget(config_name='default', attrs={'style': 'min-height: 800px;'}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            
        }
    
        labels = {
            "title": "Article Title",
            "content": "Content",
            "excerpt": "Excerpt",
            "image": "Upload Image",
            "image_alt": "Image Alt tag",
            "status": "Article Status"
        }

        image = forms.ImageField(label='Image', required=False, widget=forms.ClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'