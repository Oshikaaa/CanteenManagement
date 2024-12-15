from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('myAccount/', views.myAccount, name='myAccount'),
    
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),

    path('my_orders/', views.my_orders, name='customer_my_orders'),
    path('customer_order_detail/<int:order_number>/', views.order_detail, name='customer_order_detail'),

    path('customer_change_password/', views.customer_change_password, name='customer_change_password'),
    path('admin_change_password/', views.admin_change_password, name='admin_change_password'),

    path('user_profile/', views.user_profile, name='user_profile'),

    path('index/', views.index, name='index'),
     
 ]