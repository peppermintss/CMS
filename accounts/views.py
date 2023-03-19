from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def home_page(request):
    return render(request,"index.html")

def register_page(request,methods=['GET','POST']):
    if request.method == "POST":
        username = request.POST.get('username')
        password=request.POST.get('password')
        user= User.objects.create_user(username,password=password)
        return redirect('home-page')
    else:
        return render (request,'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            return redirect('home-page')
        else:
            return render(request,'403.html')
    else:
        return render(request,"login.html")


