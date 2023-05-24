from django.shortcuts import render, redirect, HttpResponse
from .forms import CreateUserForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
import random
from django.core.exceptions import PermissionDenied
from faculty.models import Faculty
from .perm_checkers import verify_admin_access
from faculty.models import Subject, Assignment
from .models import Account, Attendance
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone


# This block is a crime against humanity. Fix it.
def get_assignments(request, subjects):
    assignments = {}
    submitted_assignments = list((Assignment.objects.filter(submitted_by=request.user)))
    now = timezone.now().date()

    missed_assignments = list(
        Assignment.objects.filter(deadline__lte=now).exclude(
            title__in=submitted_assignments
        )
    )

    for subject in subjects:
        subject_assignments = Assignment.objects.filter(subject=subject)

        for assignment in subject_assignments:
            if (
                request.user not in assignment.submitted_by.all()
                and assignment not in missed_assignments
            ):
                if subject not in assignments:
                    print(subject)
                    assignments[subject] = []
                assignments[subject].append(assignment)

    return assignments, submitted_assignments, missed_assignments


# OO LOOK AT THIS IF ELSE LADDER OO ITS NOT GOOD PRACTICE OOO SO SCARY I CRY


# THIS FUNCTION IS EXTREMELY CLUTTERED REFACTOR PLEASE I CRY OMG SO BAD
@login_required
def dashboard(request):
    if request.method == "POST":
        user = Account.objects.get(username=request.user.username)
        new_pass = request.POST["new-password"]

        user.set_password(new_pass)
        user.save()
        messages.success(request, "Your password was changed.")
        return redirect("home-page")

    group = request.user.groups.all()[0]
    group = str(group)

    if group == "admin":
        courses = Faculty.objects.all()
        context = {"courses": courses}
        return render(request, "adash.html", context=context)

    elif group == "teacher":
        teacher_obj = Account.objects.get(username=request.user.username)
        subjects = Subject.objects.filter(teacher=teacher_obj)
        context = {"teacher": teacher_obj}

        return render(request, "tdash.html", context=context)

    # ADDING .FIRST IN SUBJECT DECLARATION RETURNS ERROR NOT ITERABLE
    else:
        """
        there might be a way to handle this better using the ORM. Search for a better way.
        """
        subjects = Subject.objects.filter(semester=request.user.semester)
        assignments, submitted_assignments, missed_assignments = get_assignments(
            request, subjects
        )
        context = {
            "subjects": subjects,
            "assignments": assignments,
            "submitted_assignments": submitted_assignments,
            "missed_assignments": missed_assignments,
        }
        return render(request, "sdash.html", context=context)


# why createuserform tho? idk i forgot why. future me don't touch it unless you are 100%
# sure on the fix.
@login_required
def register_page(request):
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
    if not get_referer(request):
        raise PermissionDenied

    form = CreateUserForm
    if request.method == "POST":
        print("posted here")
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

            return redirect(request.headers["Referer"])
        else:
            print(form.errors)

    context = {
        "form": form,
        "faculty": faculty,
        "semester": semester,
    }

    return render(request, "register.html", context)


@csrf_exempt
def delete_account(request, username):
    referer = get_referer(request)
    if not referer:
        raise PermissionDenied

    Account.objects.get(username=username).delete()
    print("Deleted")
    return redirect(referer)


@user_passes_test(verify_admin_access)
def attendance(request, faculty, semester):
    student_list = Account.objects.filter(faculty=faculty).filter(semester=semester)
    attendance_obj = Attendance.objects.get(date=timezone.now().date())
    present_students = [student for student in attendance_obj.students.all()]

    context = {
        "students": student_list,
        "present": present_students,
    }

    return render(request, "attendance.html", context=context)


def get_referer(request):
    referer = request.META.get("HTTP_REFERER")
    if not referer:
        return None
    return referer
