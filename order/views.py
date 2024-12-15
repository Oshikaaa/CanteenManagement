import json
from django.http import HttpResponseRedirect
import requests
from django.shortcuts import get_object_or_404, redirect, render
from django.core.serializers.json import DjangoJSONEncoder

from CanteenManagement.settings import KHALTI_SECRET_KEY
from food.context_processor import get_cart_amounts
from food.models import Cart, FoodItem
from order.forms import OrderForm
from order.models import FoodOrder, Order, Payment
from order.send_email import send_order_email
from order.utils import generate_order_number
from django.db.models import F

# Create your views here.
def place_order(request):
    if not request.user.is_authenticated:
        print("User is not authenticated")
        return redirect('login')
    print("User is authenticated")

    cart_items = Cart.objects.filter(user=request.user).order_by("created_at")
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect("menu")

    subtotal = get_cart_amounts(request)["subtotal"]
    total_tax = get_cart_amounts(request)["tax"]
    grand_total = get_cart_amounts(request)["grand_total"]
    tax_data = get_cart_amounts(request)["tax_dict"]

    if request.method == 'POST':
        

        form = OrderForm(request.POST)
        if form.is_valid():
            print("POST Data:")
            for key, value in request.POST.items():
                print(f"{key}: {value}")
            order = Order()
            order.first_name = form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            
            # Remove country code and keep the last 10 digits of the phone number
            phone_number = form.cleaned_data['phone']
            phone_number = phone_number
            form.cleaned_data['phone'] = phone_number
            order.phone=phone_number
            for cart_item in cart_items:
                order.food_item = cart_item.food_item
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data, cls=DjangoJSONEncoder)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save()
            order_number = generate_order_number(order.id)
            order.order_number = order_number
            order.save()

            
            # Store the modified order form data and order number in the session
            request.session['order_form_data'] = form.cleaned_data
            request.session['order_number'] = order_number
            
            # Print session data in the terminal
            print("Session Data:", request.session['order_form_data'])
            print("Order Number:", request.session['order_number'])
           
            form = OrderForm()
            context = {
                'order': order,
                'form': form,
                'cart_items': cart_items
            }
            return render(request, 'order/place_order.html', context)
        else:
            print(form.errors)

    return render(request, "order/place_order.html")





def payments(request):
    # Retrieve session data
    order_form_data = request.session.get('order_form_data')
    order_number = request.session.get('order_number')
    cart_totals = get_cart_amounts(request)
    subtotal = cart_totals['subtotal']
    grand_total = cart_totals['grand_total']

    if order_form_data:
        try:
            # Get the associated order
            order = Order.objects.get(user=request.user, order_number=order_number)

            # Prepare payment data for Khalti
            data = json.dumps({
                "return_url": "http://127.0.0.1:8000/order/verify",
                "website_url": "http://127.0.0.1:8000/",
                "amount": int(grand_total * 100),  # Amount in paisa
                "purchase_order_id": order_number,
                "purchase_order_name": "Food Order Payment",
                "customer_info": {
                    "name": f"{order_form_data['first_name']} {order_form_data['last_name']}",
                    "email": order_form_data['email'],
                    "phone": order_form_data['phone'],
                },
            })
            headers = {
                "Authorization": f"Key {KHALTI_SECRET_KEY}"  ,
                'Content-Type': 'application/json',
            }

            # Send payment initiation request
            url="https://a.khalti.com/api/v2/epayment/initiate/"

            response = requests.request("POST", url = url, headers=headers, data=data)

            print(response.status_code)  # Log the status code
            print(response.json()) 

            if response.status_code == 200:
                # Extract response data
                response_data = response.json()
                pidx = response_data.get("pidx")
                

                # Save payment record
                payment = Payment(pidx=pidx)
                payment.save()

                # Update order with payment info
                order.payment = payment
                order.is_ordered = True
                order.save()

                # Process cart items and update food item availability
                cart_items = Cart.objects.filter(user=request.user)
                for item in cart_items:
                  ordered_food = FoodOrder()
                  ordered_food.order = order
                  ordered_food.payment = payment
                  ordered_food.user = request.user
                  ordered_food.food_item = item.food_item
                  ordered_food.quantity = item.quantity
                  ordered_food.price = item.food_item.total_cost
                  ordered_food.amount = item.food_item.total_cost * item.quantity
                  ordered_food.save()

                return HttpResponseRedirect(response_data.get("payment_url"))

        except Order.DoesNotExist:
            # Handle case where order is not found
            return render(request, 'food/pay_error.html', {
                "error": "Order not found. Please try again."
            })

        except Exception as e:
            # Handle any other exceptions
            print(f"Error during payment processing: {e}")
            return render(request, 'food/pay_error.html', {
                "error": "An unexpected error occurred. Please try again."
            })

    # Handle missing session data
    return render(request, 'food/pay_error.html', {
        "error": "Order form data is missing. Please try again."
    })


from django.db import IntegrityError

def verify(request):
    pidx = request.GET.get('pidx')
    order_number = request.GET.get('purchase_order_id')

    if not pidx or not order_number:
        return render(request, 'food/pay_error.html', {"error": "Invalid payment or order details."})

    data = {
        "pidx": pidx
    }
    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}"
    }

    response = requests.post("https://a.khalti.com/api/v2/epayment/lookup/", json=data, headers=headers)
    data = response.json()
    status = data.get("status")
    updated_pidx = data.get("pidx")

    try:
        order = Order.objects.get(user=request.user, order_number=order_number)

        if status == 'Completed':
            # Check if payment already exists
            payment, created = Payment.objects.get_or_create(
                pidx=updated_pidx,
                defaults={"payment_status": {"status": status, "pidx": updated_pidx}}
            )

            # Update order if payment was created
            if created:
                order.payment = payment
                order.is_ordered = True
                order.save()

                
            # Send payment verification email
            send_order_email(order, order.email, 'verified')

            # Clear the cart
            Cart.objects.filter(user=request.user).delete()

            return redirect('order_complete', order_id=order.id)

        return render(request, 'food/pay_error.html', {"error": "Order not found."})

    except Order.DoesNotExist:
        return render(request, 'food/pay_error.html', {"error": "Order not found."})

    except IntegrityError:
        return render(request, 'food/pay_error.html', {"error": "Duplicate payment detected. Please contact support."})

    except Exception as e:
        print(f"Error during payment verification: {e}")
        return render(request, 'food/pay_error.html', {"error": "An unexpected error occurred. Please try again."})





def order_complete(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)
    ordered_product = FoodOrder.objects.filter(order=order)

    subtotal = sum(item.price * item.quantity for item in ordered_product)
    
    context = {
        'order': order,
        'ordered_product': ordered_product,
        'subtotal': subtotal
    }
    return render(request, 'order/order_complete.html', context)



def calculate_tax_total(tax_data):
    tax_total = 0
    for tax_type, tax_values in tax_data.items():
        for percentage, tax_amount in tax_values.items():
            tax_total += float(tax_amount)
    return tax_total