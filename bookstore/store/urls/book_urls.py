"""
URLs for book module
"""
from django.urls import path
from store.controllers.bookController import views

app_name = 'book'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('<str:book_id>/', views.detail, name='detail'),
]