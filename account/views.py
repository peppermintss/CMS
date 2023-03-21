from django.shortcuts import render,redirect

from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required


def dashboard(request):
    print(request.user.groups.all()[0])
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


# Create your views here.
