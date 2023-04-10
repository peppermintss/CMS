from django.shortcuts import render, redirect, HttpResponse
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
import random
from django.core.exceptions import PermissionDenied
from faculty.models import Faculty
from .perm_checkers import verify_admin_access
from faculty.models import Subject
from .models import Account

# OO LOOK AT THIS IF ELSE LADDER OO ITS NOT GOOD PRACTISE OOO SO SCARY I CRY


# THIS FUNCTION IS EXTREMELY CLUTTERED REFACTOR PLEASE I CRY OMG SO BAD
@login_required
def dashboard(request):
    group = request.user.groups.all()[0]
    group = str(group)
    if group == "admin":
        courses = Faculty.objects.all()
        context = {"courses": courses}
        return render(request, "adash.html", context=context)
    elif group == "teacher":
        teacher_obj = Account.objects.get(username=request.user.username)
        subjects = Subject.objects.filter(teacher=teacher_obj)
        context = {"subjects": subjects}
        return render(request, "tdash.html", context=context)
    else:
        subjects = Subject.objects.filter(semester=request.user.semester)
        context = {"subjects": subjects}
        return render(request, "sdash.html", context=context)


# why createuserform tho? idk i forgot why. future me don't touch it unless you are 100%
# sure on the fix.
@login_required
def register_page(request, methods=["GET", "POST"]):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("home-page")
        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "register.html", context)


# This function is very very ugly but it works. Maybe override the save() method instead and make it cleaner?


@user_passes_test(verify_admin_access)
def add_account(request, faculty, semester):
    print("ran")
    if not get_referer(request):
        raise PermissionDenied

    form = CreateUserForm
    if request.method == "POST":
        group = "teacher" if faculty == "teacher" else "student"
        form = CreateUserForm(request.POST)
        if form.is_valid():
            new_account = form.save(commit=False)
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            phone_number = form.cleaned_data["phone_number"]

            new_account.username = (
                f"{first_name + last_name + str(random.randint(1,100))}".lower()
            )
            new_account.set_password(str(phone_number))
            new_account.faculty = faculty
            new_account.semester = semester

            new_account.save()
            group = Group.objects.get(name=f"{group}")
            new_account.groups.add(group)
            print(request.headers["Referer"])
            return redirect(request.headers["Referer"])
        else:
            print(form.errors)

    context = {
        "form": form,
        "faculty": faculty,
        "semester": semester,
    }

    return render(request, "register.html", context)


def get_referer(request):
    referer = request.META.get("HTTP_REFERER")
    if not referer:
        return None
    return referer
