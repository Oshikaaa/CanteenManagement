import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from account.models import User
from order.models import Order
from django.contrib.auth.decorators import login_required, user_passes_test

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


@login_required(login_url='login')
@user_passes_test(lambda user: user.role == User.ADMIN)
def send_order_ready_email(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if order.status != "Completed":
        try:
            # Send email
            send_mail(
                subject="Your Order is Ready",
                message=f"""
                Dear {order.first_name},\n
                Your order with order number {order.order_number} is now ready for pickup or delivery.\n
                Thank you for shopping with us!\n\n
                Best regards,\n
                Canteen Management Team
                """,
                from_email="your_email@gmail.com",  # Update with your email
                recipient_list=[order.email],
                fail_silently=False,
            )

            # Update the order status to "Completed"
            order.status = "Completed"
            order.save()

            messages.success(request, f"Order ready email sent to {order.email}!")

        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")
    else:
        messages.info(request, f"Order {order.order_number} is already marked as Completed.")

    return redirect('pending_orders')