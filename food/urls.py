from django.urls import path, include
from . import views


urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/' , views.checkout,name='checkout'),
    path('get_cart_details/', views.get_cart_details, name='get_cart_details'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),  # Delete cart item
 ]