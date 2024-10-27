from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('myAccount/', views.myAccount, name='myAccount'),
    
    path('custDashboard/', views.custDashboard, name='custDashboard'),
    path('adminDashboard/', views.adminDashboard, name='adminDashboard'),

    path('index/', views.index, name='index'),
     
 ]