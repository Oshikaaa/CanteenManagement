from datetime import timezone
from venv import logger
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import FoodItemForm
from order.forms import OrderForm
from account.models import UserProfile

from . context_processor import get_cart_amounts, get_cart_counter
from food.models import Cart, Category, FoodItem
from django.db.utils import IntegrityError
from django.contrib import messages

from django.utils.text import slugify
from django.db.models import Count , Prefetch

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


def add_food(request):
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_name = form.cleaned_data['food_name'].strip().lower()  # Clean the name (strip whitespace, lowercase)
            product = form.save(commit=False)

            # Generate slug
            slug = slugify(food_name)

            # Ensure the slug is unique by checking if it already exists
            if FoodItem.objects.filter(slug=slug).exists():
                slug = f"{slug}-{timezone.now().strftime('%Y%m%d%H%M%S')}"

            # Check if food_name already exists (if that's the problem)
            if FoodItem.objects.filter(food_name__iexact=food_name).exists():
                messages.error(request, 'A product with this name already exists. Please choose a different name.')
                return redirect("add_food")

            product.slug = slug
            product.user = request.user

            try:
                product.save()
                messages.success(request, 'Product Item added successfully!')
                return redirect("product_builder")
            except Exception as e:
                messages.error(request, f'Error {e}')
                return redirect("add_food")
        else:
            print(form.errors)
    else:
        form = FoodItemForm()
    context = {
        'form': form,
    }
    return render(request, 'food/add_food.html', context)



def edit_product(request, pk=None):
    product = get_object_or_404(FoodItem, pk=pk)
    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            productTitle = form.cleaned_data['food_name']
            product = form.save(commit=False)
            product.slug = slugify(productTitle)
            form.save()
            messages.success(request, 'Product Item updated successfully!')
            return redirect('product_category', product.category.id)
        else:
            print(form.errors)

    else:
        form = FoodItemForm(instance=product)
        # form.fields['category'].queryset = Category.objects.f
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'food/edit_food.html', context)




def product_builder(request):
    # Prefetch related products for each category
    categories = Category.objects.annotate(num_products=Count('fooditem')).prefetch_related(
        Prefetch('fooditem_set', queryset=FoodItem.objects.all())
    ).order_by('created_at')
    
    for category in categories:
        print(category.fooditem_set.all())  # Debug: print related products for each category
    
    context = {
        'categories': categories,
    }
    return render(request, 'food/product_builder.html', context)


def productItem_by_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    productItems = FoodItem.objects.filter(category=category)
    print(productItems.query)  # Print the SQL query
    
    context = {
        'productItems': productItems,
        'category': category,
    }
    return render(request, 'food/productItem_by_category.html', context)



def product_detail(request, id):
    # Get the current food item
    food_item = get_object_or_404(FoodItem, id=id)

    # Fetch related food items based on the same category, excluding the current food item
    related_food_items = FoodItem.objects.filter(category=food_item.category).exclude(id=food_item.id)[:3]

    # Fetch most popular food items based on some logic (e.g., number of times marked as sold out)
    popular_food_items = FoodItem.objects.annotate(
        popularity=Count('is_soldout')
    ).order_by('-popularity')[:3]

    # Fetch user's cart items if authenticated
    cart_items = Cart.objects.filter(user=request.user) if request.user.is_authenticated else None

    context = {
        'food_item': food_item,
        'related_food_items': related_food_items,
        'popular_food_items': popular_food_items,
        'cart_items': cart_items,
    }
    return render(request, "food/product_detail.html", context)