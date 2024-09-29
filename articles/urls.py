from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('add/', views.add_article, name='add_article'),
    path('admin_articles_view/', views.admin_articles_view, name='admin_articles_view'),
    path('edit/<slug:slug>/', views.edit_article, name='edit_article'),
    path('delete/<slug:slug>/', views.delete_article, name='delete_article'),
    path('<slug:slug>/', views.article, name='article'),
]