"""
Views for customer module
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from store.models.customer.models import Customer


def login(request):
    """
    Customer login view
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # In a real application, you would authenticate against your User model
        # For now, we'll simulate authentication
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('book:index')
            else:
                messages.error(request, 'Invalid credentials')
        except:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'customer/login.html')


def register(request):
    """
    Customer registration view
    """
    if request.method == 'POST':
        # Process registration form
        username = request.POST['username']
        password = request.POST['password']
        fullname = request.POST['fullname']
        email = request.POST['email']
        
        # In a real application, you would create a User and Customer object
        # For now, we'll simulate registration
        messages.success(request, 'Registration successful! Please login.')
        return redirect('customer:login')
    
    return render(request, 'customer/register.html')


def profile(request):
    """
    Customer profile view
    """
    if request.user.is_authenticated:
        # Get customer info
        try:
            customer = Customer.objects.get(user=request.user)
            context = {
                'customer': customer
            }
        except Customer.DoesNotExist:
            context = {}
        
        return render(request, 'customer/profile.html', context=context)
    else:
        messages.error(request, 'Please login to view your profile')
        return redirect('customer:login')


def logout(request):
    """
    Customer logout view
    """
    auth_logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('book:index')