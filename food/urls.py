from django.urls import path, include
from . import views
from recommendation.views import recommend_view


urlpatterns = [
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('checkout/' , views.checkout,name='checkout'),
    path('get_cart_details/', views.get_cart_details, name='get_cart_details'),
    
    path('add_food/', views.add_food, name='add_food'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    
    path('product_builder/', views.product_builder, name='product_builder'),
    path('product_category/<int:pk>/', views.productItem_by_category, name='product_category'),
    path('product_detail/<int:id>/' , views.product_detail,name='product_detail'),

    path('recommend/', recommend_view, name='recommend'),


    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:product_id>/', views.decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', views.delete_cart, name='delete_cart'),  # Delete cart item
 ]