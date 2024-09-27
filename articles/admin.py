from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'posted_date', 'is_deleted')
    list_filter = ('status', 'is_deleted')