from django import forms
from .models import Article
from django_summernote.widgets import SummernoteWidget


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
            'content': SummernoteWidget(),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'