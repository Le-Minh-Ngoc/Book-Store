"""
URLs for staff module
"""
from django.urls import path
from store.controllers.staffController import views

app_name = 'staff'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-book/', views.add_book, name='add_book'),
    path('inventory/', views.inventory, name='inventory'),
]