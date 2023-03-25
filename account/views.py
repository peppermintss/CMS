from django.shortcuts import render,redirect, HttpResponse
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
import random
#OO LOOK AT THIS IF ELSE LADDER OO ITS NOT GOOD PRACTISE OOO SO SCARY I CRY

@login_required
def dashboard(request):
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
        else:
            print (form.errors)
    context = {'form':form}
    return render (request,'register.html',context)

#This function is very very ugly but it works. Maybe override the save() method instead and make it cleaner?

def add_student(request):

    faculty = request.headers['Referer']
    faculty = faculty.replace("http://127.0.0.1:8000/", "").strip("/")
    form = CreateUserForm()
    if request.method == "POST":
        form= CreateUserForm(request.POST)
        if form.is_valid():
            
            group = "teacher" if faculty=="teacher" else "student"
            student = form.save(commit=False)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data ['last_name']
            phone_number = form.cleaned_data['phone_number']
            semester = form.cleaned_data['semester']
            student.username = f"{first_name + last_name + str(random.randint(1,100))}"
            student.set_password(str(phone_number))
            student.faculty = faculty
            
            if faculty =="teacher":
                semester = 0
            student.semester = semester
            student.save()
            group= Group.objects.get(name=f"{group}")
            student.groups.add(group)
            
        else:
            print (form.errors)
    context = {'form':form,'faculty':faculty}
    return render (request,'register.html',context)

# Create your views here.
