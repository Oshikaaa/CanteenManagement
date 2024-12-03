from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
from django.contrib import messages, auth

from account.forms import UserForm
from account.models import User, UserProfile
from account.utils import detectUser

from django.contrib.auth import authenticate, login as auth_login

from food.models import Category

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
    
    return render(request, 'account/custDashboard.html' )


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