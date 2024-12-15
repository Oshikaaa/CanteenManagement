from datetime import date
import json
from django.shortcuts import get_object_or_404, redirect, render

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
from django.contrib import messages, auth

from account.forms import UserForm
from account.models import User, UserProfile
from account.utils import detectUser

from .forms import  UserChangeForm, UserForm , CustomPasswordChangeForm, UserProfileForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth import authenticate, login as auth_login

from food.models import Category
from order.models import FoodOrder, Order
from django.db.models import Sum

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    if user.is_authenticated:
        redirect_url = detectUser(user)
        if redirect_url:
            return redirect(redirect_url)
        else:
            messages.error(request, 'Unable to determine dashboard for the user.')
            return redirect('login')
    else:
        messages.error(request, 'You need to log in to access your account.')
        return redirect('login')
    

def check_role_admin(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.is_active = True
            user.save()

            messages.success(request, 'Your account has been registered successfully!')
            return redirect('login')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)




def login(request):
    
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(user)
        if user is not None and user.is_active:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'login.html')




def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('login')





@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    user = request.user

    # Total Orders Count
    orders_count = Order.objects.filter(user=user).count()

    # Current User's Most Ordered Food
    most_ordered_food = (
        FoodOrder.objects.filter(user=user)
        .values('food_item__food_name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
        .first()
    )

    # Current User's Most Ordered Category
    most_ordered_category = (
        FoodOrder.objects.filter(user=user)
        .values('food_item__category__category_name')
        .annotate(total_quantity=Sum('quantity'))
        .order_by('-total_quantity')
        .first()
    )

    # Total Amount Spent
    total_spent = (
        FoodOrder.objects.filter(user=user)
        .aggregate(total_spent=Sum('amount'))
        .get('total_spent', 0) or 0
    )

    orders_with_food = (
        Order.objects.filter(user=user)
        .prefetch_related('foodorder_set')
        .order_by('-created_at')
    )

    context = {
        'user': user,
        'orders_count': orders_count,
        'most_ordered_food': most_ordered_food['food_item__food_name'] if most_ordered_food else "N/A",
        'most_ordered_category': most_ordered_category['food_item__category__category_name'] if most_ordered_category else "N/A",
        'total_spent': total_spent,
        'orders_with_food': orders_with_food,
    }
    return render(request, 'account/custDashboard.html' , context )


@login_required(login_url='login')
@user_passes_test(check_role_admin)
def adminDashboard(request):

    return render(request, 'account/adminDashboard.html' )





def index(request):
    category = Category.objects.all()

    context = {
        "category" : category 
    }

    return render(request , "index.html" , context)




@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user

            if user.role == 2:
                return redirect('custDashboard')
    else:
        # Pass user=request.user to initialize the form with the user's data
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(check_role_admin)
def admin_change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session
            messages.success(
                request, 'Your password was successfully updated!')
            logout(request)  # Log out the user

            if user.role == 1:
                return redirect('adminDashboard')
    else:
        # Pass user=request.user to initialize the form with the user's data
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'account/change_password.html', {'form': form})




@login_required(login_url='login')
@user_passes_test(check_role_customer)
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'account/my_orders.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_product = FoodOrder.objects.filter(order=order).order_by('-created_at')
        subtotal = 0
        for item in ordered_product:
            subtotal += (item.price * item.quantity)
        context = {
            'order': order,
            'ordered_product': ordered_product,
            'subtotal': subtotal,
        }
    except json.JSONDecodeError as e:
        print(f"Error decoding tax_data: {str(e)}")
    
    return render(request, 'account/order_detail.html', context)



@login_required(login_url='login')
@user_passes_test(check_role_customer)
def user_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        user_form = UserChangeForm(request.POST, instance=user)

        if profile_form.is_valid():
            profile_form.save()
            return redirect("user_profile")
    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserChangeForm(instance=user)

    context = {
        "profile_form": profile_form,
        "user_form": user_form,
        "profile": user_profile,  # Include profile in context
    }
    return render(request, "account/user_profile.html", context)