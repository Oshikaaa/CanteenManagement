from venv import logger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from order.forms import OrderForm
from account.models import UserProfile

from . context_processor import get_cart_amounts, get_cart_counter
from food.models import Cart, FoodItem

# Create your views here.
def menu(request):
  food_items = FoodItem.objects.all()

  context = {
      "food_items" : food_items
  }
  return render(request , "food/menu.html" , context)


def get_cart_details(request):
    cart_items = Cart.objects.filter(user=request.user)
    product_quantities = {item.food_item.id: item.quantity for item in cart_items}
    
    return JsonResponse({
        'product_quantities': product_quantities,
    })


def cart(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = sum(item.food_item.total_cost * item.quantity for item in cart_items)
        grand_total = subtotal  # Add taxes or other calculations as needed
        tax_dict = {}  # Add your tax calculations here

        context = {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'grand_total': grand_total,
            'tax_dict': tax_dict
        }
        return render(request, 'food/cart.html', context)
    return redirect('login')



def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = FoodItem.objects.get(id=product_id)

                # Check if the user has already added this product to the cart
                cart_item, created = Cart.objects.get_or_create(user=request.user, food_item=product)

                if created:
                    # Ensure the quantity is set to 1 when the item is newly added to the cart
                    cart_item.quantity = 1
                    cart_item.save()
                    message = 'Added to cart'
                    return redirect("cart")
                else:
                    # If the item already exists in the cart, increment the quantity
                    cart_item.quantity += 1
                    cart_item.save()
                    message = 'Increased quantity in cart'

                return JsonResponse({
                    'status': 'Success',
                    'message': message,
                    'qty': cart_item.quantity
                })
            except FoodItem.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'This product does not exist!'})
            except Exception as e:
                logger.error(f"Unexpected error in add_to_cart: {e}")
                return JsonResponse({'status': 'Failed', 'message': 'An unexpected error occurred'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})




def decrease_cart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                product = FoodItem.objects.get(id=product_id)
                cart_item = Cart.objects.get(user=request.user, food_item=product)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
                return JsonResponse({
                    'status': 'Success',
                    'cart_counter': get_cart_counter(request),
                    'cart_amount': get_cart_amounts(request)
                })
            except Cart.DoesNotExist:
                return JsonResponse({'status': 'Failed', 'message': 'Item not found in cart!'})
        return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})
    return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})



def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # Check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request) ,'redirect_url': reverse('cart')})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid request!'})


def checkout(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('shop')
    
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address
    }
    form = OrderForm(initial=default_values)
    context = {
        'form': form,
        'cart_items': cart_items,
    }
    return render(request,'food/checkout.html',context )
