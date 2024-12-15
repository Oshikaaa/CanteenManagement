from django.urls import path, include
from . import views

from order.send_email import send_order_ready_email


urlpatterns = [
     path('place_order/', views.place_order, name='place_order'),
     path('payments/', views.payments, name='payments'),
     path('verify/', views.verify , name='verify'),
     path('send_order_ready_email/<int:order_number>', send_order_ready_email , name='send_order_ready_email'),
     path('order_complete/<int:order_id>', views.order_complete, name='order_complete'),
     path('pending_orders', views.pending_orders, name='pending_orders'),
     
 ]