from django.contrib import admin
from .models import Faq
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Faq)
class ArticleAdmin(SummernoteModelAdmin):
    summernote_fields = ('answer',)
    list_display = ('question', 'id')