from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import *


# Create your views here.
def home(request):
    return render(request,'home.html')
def login(request):
    if request.method=='POST':
        username=request.POST['name']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect("/")
        else:
            messages.error(request,"User does not exists")
            return render(request,'login.html')
    else:
        return render(request,'login.html')
def signup(request):    
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username already exists!!')
                return render(request,'signup.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'Email already exists!!')
                return render(request,'signup.html')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                user.save()
                messages.success(request,"Sign Up Successfully")
                return redirect("/login/")
        else:
            messages.error(request,'Passwords does not match')
    else:
        return render(request,'signup.html')
def logout(request):
    auth.logout(request)
    return redirect('/')

def products(request):
    categories=Categories.objects.all()
    active_categories=[]
    p_list=[]
    if request.method=='POST':
        for i in categories:
            if i.name in request.POST:
                active_categories.append(i)
        if len(active_categories)==0:
            active_categories=categories
        
    else:
        active_categories=categories
    for c in active_categories:
        ls=Products.objects.filter(category=c)
        for i in ls:
            p_list.append(i)
    context={
        'p_list':p_list,
        'categories':categories
    }
    return render(request,'products.html',context)
def item(request,pk):
    obj=Products.objects.filter(product_id=pk)
    return render(request,'item.html',{'obj':obj})

@login_required
def cart(request):
    obj=Cart.objects.filter(user=request.user)
    return render(request,'cart.html',{'obj':obj})
@login_required
def add_to_cart(request,pk):
    pr=Products.objects.filter(product_id=pk)[0]
    cart=Cart.objects.filter(user=request.user,product=pr)

    if not cart.exists():
        obj=Cart(user=request.user,product=pr,quantity=1)
        obj.save()
    else:
        temp=(int)(cart[0].quantity)
        temp=temp+1
        cart=cart.first()
        cart.delete()
        Cart(user=request.user,product=pr,quantity=temp).save()
        # cart.quantity=temp
        # cart.save()
    return redirect('/cart/')
def cart_remove(request,pk):
    obj=Cart.objects.filter(cart_id=pk)
    obj.delete()
    return redirect('/cart/')
def checkout(request):
    obj=Cart.objects.filter(user=request.user)
    sum=0
    for i in obj:
        sum=sum+(i.product.price)*(i.quantity)
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone_no=request.POST['phone']
        shipping_address=request.POST['address']
        cust=Customers(first_name=first_name,last_name=last_name,email=email,phone_no=phone_no,shipping_address=shipping_address)
        cust.save()
        order=Orders(user=request.user,customer=cust,total_amount=sum)
        order.save()
        carts=Cart.objects.filter(user=request.user)
        for cart in carts:
            order_item=OrderItems(order=order,product=cart.product,quantity=cart.quantity,subtotal=(cart.product.price)*(cart.quantity))
            order_item.save()
        carts.delete()
        messages.success(request,"Order Placed :)")
        return redirect('/products/')
    else: 
        return render(request,'checkout.html',{'obj':obj,'sum':sum})

def profile(request):
    user=request.user
    orders=Orders.objects.filter(user=user)
    list=[]
    for i in orders:
        order_item=OrderItems.objects.filter(order=i)
        # l=[]
        # for j in order_item:
        #     l.append(j)
        list.append(order_item)
    my_zip=zip(list,orders)
    context={
        'my_zip':my_zip,
        'user':user
    }
    return render(request,'profile.html',context)
@login_required
def buy(request,pk):
    obj=Products.objects.filter(product_id=pk)
    sum=obj[0].price
    if request.method=='POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        phone_no=request.POST['phone']
        shipping_address=request.POST['address']
        cust=Customers(first_name=first_name,last_name=last_name,email=email,phone_no=phone_no,shipping_address=shipping_address)
        cust.save()
        order=Orders(user=request.user,customer=cust,total_amount=sum)
        order.save()
        order_item=OrderItems(order=order,product=obj[0],quantity=1,subtotal=obj[0].price)
        order_item.save()
        messages.success(request,"Order Placed :)")
        return redirect('/products/')
    else: 
        return render(request,'buy.html',{'obj':obj,'sum':sum})
