from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.faqs, name='faq'),
    path('add/', views.add_faq, name='add_faq'),
]