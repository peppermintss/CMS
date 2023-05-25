from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from account.models import Account
from .forms import FacultyAddForm, SubjectAddForm, AssignmentAddForm
from .models import Faculty, Subject, Assignment
from django.contrib.auth.decorators import login_required, user_passes_test
from account.perm_checkers import verify_admin_access
from django.views.decorators.csrf import csrf_exempt


@login_required
@user_passes_test(verify_admin_access)
def get_students_by_semester(request, faculty, semester):
    if faculty == "teacher":
        teachers = Account.objects.filter(faculty=faculty)
        context = {"teachers": teachers}
        return render(request, "teacher_list.html", context=context)

    allowed_faculty = [faculty.name.lower() for faculty in Faculty.objects.all()]

    subjects = Subject.objects.filter(faculty=faculty.upper()).filter(semester=semester)

    if semester > 8 or faculty not in allowed_faculty:
        raise Http404
    else:
        students = Account.objects.filter(faculty=faculty).filter(semester=semester)
        context = {
            "faculty": faculty,
            "students": students,
            "semester": semester,
            "subjects": subjects,
            "semesters": range(1, 9),
        }
        return render(request, "student-by-semester.html", context=context)


@login_required
@user_passes_test(verify_admin_access)
def add_course(request):
    form = FacultyAddForm
    if request.method == "POST":
        form = FacultyAddForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "add_course.html", {"form": form})


def add_subject(request, faculty, semester):
    faculty = faculty.lower()
    form = SubjectAddForm
    if request.method == "POST":
        print("posted")
        form = SubjectAddForm(request.POST)
        if form.is_valid():
            new_subject = form.save(commit=False)
            new_subject.name = new_subject.name.lower()
            new_subject.faculty = Faculty.objects.get(name=faculty.upper())
            new_subject.semester = semester
            new_subject.save()
            return redirect(request.headers["Referer"])
    context = {"form": form, "faculty": faculty, "semester": semester}
    return render(request, "add_subject.html", context=context)


# WHEN PASSING STRING IN CONTEXT MAKE SURE TO WRAP IT IN STR() OR ELSE IT WONT WORK.
def subject_detail_view(request, subject):
    group = request.user.groups.all()[0]
    subject_obj = Subject.objects.get(name=subject.lower())
    context = {"subject": subject_obj, "group": str(group)}
    if request.method == "POST":
        subject_obj.notice = request.POST["notice"]
        subject_obj.save()
    return render(request, "subject_detail.html", context=context)


# ONLY WORKS FOR PDF. MAYBE USE MIME TO CHANGE
def download(request, filename):
    response = HttpResponse(open(f"media/{filename}", "rb").read())
    response["Content-Type"] = "application/pdf"
    response["Content-Disposition"] = "attachment"
    return response


@csrf_exempt
@login_required
def submit_assignment(request, pk):
    assignment = Assignment.objects.get(id=pk)

    print("Submitted")
    assignment.submitted_by.add(request.user)
    referrer = get_referer(request)

    return redirect(referrer)


def add_assignment(request, subject):
    form = AssignmentAddForm()
    if request.method == "POST":
        form = AssignmentAddForm(request.POST, request.FILES)

        if form.is_valid():
            new_assignment = form.save(commit=False)
            new_assignment.subject = Subject.objects.get(name=subject.upper())
            new_assignment.save()

            return redirect(request.headers["Referer"])
        else:
            print(form.errors)

    context = {
        "form": form,
        "subject": subject,
    }

    return render(request, "add_assignment.html", context=context)


def assignment_detail(request, pk):
    return render(request, "assignment_detail.html")


def get_referer(request):
    referer = request.META.get("HTTP_REFERER")
    if not referer:
        return None
    return referer
