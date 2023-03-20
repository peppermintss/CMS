from django.shortcuts import render,redirect

from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CreateUserForm
import random

def home_page(request):
    return render(request,"index.html")

def register_page(request,methods=['GET','POST']):
    form = CreateUserForm()
    if request.method == "POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home-page")
    context = {'form':form}
    return render (request,'register.html',context)

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

from django.shortcuts import render

# Create your views here.
