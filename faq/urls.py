from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.faqs, name='faq'),
    path('add/', views.add_faq, name='add_faq'),
    path('delete/<int:id>/', views.delete_faq, name='delete_faq'),
    path('edit/<int:id>/', views.edit_faq, name='edit_faq'),  
]