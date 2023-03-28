from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import random
from django.core.exceptions import PermissionDenied
from faculty.models import Course
#OO LOOK AT THIS IF ELSE LADDER OO ITS NOT GOOD PRACTISE OOO SO SCARY I CRY

@login_required
def dashboard(request):
    group = request.user.groups.all()[0]
    group = str(group)
    if group == "admin":
        courses = Course.objects.all()

        return render(request,"adash.html",{'courses':courses})
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
        else:
            print (form.errors)
    context = {'form':form}
    return render (request,'register.html',context)

#This function is very very ugly but it works. Maybe override the save() method instead and make it cleaner?


def add_account(request,faculty,semester):
    if not get_referer(request):
        raise PermissionDenied
    print(faculty,semester)
    form = CreateUserForm
    if request.method == "POST":
        group = "teacher" if faculty=="teacher" else "student"
        form= CreateUserForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data ['last_name']
            phone_number = form.cleaned_data['phone_number']
            
            new_account.username = f"{first_name + last_name + str(random.randint(1,100))}".lower()
            new_account.set_password(str(phone_number))
            new_account.faculty = faculty
            new_account.semester = semester
           
            new_account.save()
            group= Group.objects.get(name=f"{group}")
            new_account.groups.add(group)
            print(request.headers['Referer'])
            return redirect(request.headers['Referer'])
        else:
            print(form.errors)

    context = {
        'form':form,
        'faculty':faculty,
        'semester':semester,
        }
    return render (request,'register.html',context)

def get_referer(request):
    referer = request.META.get('HTTP_REFERER')
    if not referer:
        return None
    return referer