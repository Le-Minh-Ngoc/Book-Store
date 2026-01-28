"""
URLs for order module
"""
from django.urls import path
from store.controllers.orderController import views

app_name = 'order'
urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<str:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<str:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('history/', views.order_history, name='order_history'),
    path('recommendations/', views.recommendations, name='recommendations'),
]