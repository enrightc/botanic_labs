from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.articles, name='articles'),
    path('add_article/', views.add_article, name='add_article'),
    path('admin_articles_view/', views.admin_articles_view, name='admin_articles_view'),
    path('<slug:slug>/', views.article, name='article'),
]