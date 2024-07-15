from django.http import JsonResponse
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.shortcuts import redirect
from shop.forms import CustomUserForm
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,'shop/index.html',{"products":products})

def add_to_cart(request):
    if request.headers.get('x-requested-with')=='XMLHttpRequest':
        if request.user.authenticated:
            data=json.load(request)
            product_qty=(data['product_qty'])
            product_id=int(data['pid'])
            #print(request.user.id)
            product_status=Product.objects.get(id=product_id)
            if product_status:
                if Cart.objects.filter(user=request.user.id,product_id=product_id):
                    return JsonResponse({'status': 'Product Already in Cart'},status=200)
                else:
                    if product_status.quantity>=product_qty:
                        Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                        return JsonResponse({'status': 'Product Added in Cart'},status=200)
                    else:
                        return JsonResponse({'status':'Product stock not Available'},status=200)
        else:
            return JsonResponse({'status':'Login to Add Cart'},status=200)
    else:
        return JsonResponse({'status':'Invalid Access'},status=200)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST':
            Email=request.POST.get('email')
            pwd=request.POST.get('password')
            user=authenticate(request,email=Email,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,'Login is successfull')
                return redirect("/")
            else:
                messages.error(request,'Invalid username or Password')
                return redirect('/login')
        return render(request,'shop/login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout is successfull")
    return redirect("/")

def register(request):
    form=CustomUserForm()
    if request.method =='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,' Registration are Successfully Registered Now you cna Login...!')
            return redirect('/login')
    return render(request,'shop/register.html',{'form':form})


def collections(request):
    Catagory=catagory.objects.filter(status=0)
    return render(request,'shop/collection.html',{"Catagory":Catagory})

def collectionsview(request,name):
    if(catagory.objects.filter(name=name,status=0)):
        products=Product.objects.filter(catagory__name=name)
        return render(request,'shop/products/index.html',{"products":products,"catagory__name":name})
    else:
        messages.warning(request,"No such catagory found")
        return redirect('collections')
    
def product_details(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)):
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,'shop/products/product_details.html',{"products":products})
        else:
            messages.error(request,"NO such Product Present")
            return redirect('collections')
        
    else:
        messages.error(request,"NO such catagory Present")
        return redirect('collections')

    