from django.contrib import admin
from .models import Product, Season

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'season',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku',)

class SeasonAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )

admin.site.register(Product, ProductAdmin)
admin.site.register(Season, SeasonAdmin)
