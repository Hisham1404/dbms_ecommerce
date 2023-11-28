from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 
from .forms import SignUpForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse
from django.shortcuts import get_object_or_404


# Create your views here.

def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'cartItems':cartItems}
    return render(request, 'home.html',context)


def contact(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    context = {'cartItems':cartItems}
    return render(request, 'contact.html',context)




def shop(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'shop.html',context)


def cart(request):
    return render(request, 'cart.html',{})



def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,("You have been logged in successfully"))
            return redirect('home')
        else:
            messages.success(request,("There is an error, Please try again"))
            return redirect('login')
    else:
        return render(request, 'login.html',{})



def logout_user(request):
    logout(request)
    messages.success(request, ("YOu have been logged out"))
    return redirect('home')



def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request, user)
            messages.success(request, ("YOu have been Registered successfully"))
            return redirect('home')
        else:
            print(form.errors)
            messages.success(request, ("There was a problem please try again "))
            return redirect('register')

    else:
        return render(request, 'register.html',{'form': form})
    



def detail(request,pk):
    product = Product.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'detail.html',context)



@login_required(login_url='login')
def cart_summary(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
		#Create empty cart for now for non-logged in user
        items = []

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'cart_summary.html', context)



@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
		#Create empty cart for now for non-logged in user
        items = []


    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']

        user_shipping = ShippingAddress(
            first_name = first_name,
            last_name = last_name,
            address = address,
            city = city,
            state = state,
            zipcode = zipcode,
            customer=request.user.customer,
            
        )
        
        user_shipping.save()
         

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html',context)

@login_required(login_url='login')
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)



@login_required(login_url='login')
def payment(request):
    shipping_details = ShippingAddress.objects.filter(customer=request.user.customer)
    context = {'shipping_details':shipping_details}
    return render(request, 'payment.html',context)

