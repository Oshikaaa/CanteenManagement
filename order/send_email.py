import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from CanteenManagement import settings
from order.models import FoodOrder

def send_order_email(order, user_email, status):
    ordered_products = FoodOrder.objects.filter(order=order)
    subtotal = sum(item.price * item.quantity for item in ordered_products)
    tax_data = json.loads(order.tax_data)

    context = {
        'order': order,
        'order_number': order.order_number,
        'user': order.user,
        'ordered_products': ordered_products, 
        'subtotal': subtotal,
        'tax_data': tax_data,
        'status': status,
    }

    print("context" , context)

    subject = f"Order #{order.order_number} - {status.capitalize()}"
    html_message = render_to_string('order/order_email_template.html', context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.EMAIL_HOST_USER,
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )
