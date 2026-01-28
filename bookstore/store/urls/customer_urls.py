"""
URLs for customer module
"""
from django.urls import path
from store.controllers.customerController import views

app_name = 'customer'
urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
]