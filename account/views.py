from django.shortcuts import render,redirect

from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required

#OO LOOK AT THIS IF ELSE LADDER OO ITS NOT GOOD PRACTISE OOO SO SCARY I CRY

@login_required
def dashboard(request):
    print(request.user.is_authenticated)
    group = request.user.groups.all()[0]
    group = str(group)
    if group == "admin":
        return render(request,"adash.html")
    elif group=="teacher":
        return render(request,'tdash.html')
    else:
        return render(request,"sdash.html")
   
#why createuserform tho? idk i forgot why. future me don't touch it unless you are 100% 
#sure on the fix.

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
