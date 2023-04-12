from django.shortcuts import render, redirect
from django.http import Http404
from account.models import Account
from .forms import FacultyAddForm, SubjectAddForm
from .models import Faculty, Subject
from django.contrib.auth.decorators import login_required, user_passes_test
from account.perm_checkers import verify_admin_access


@login_required
@user_passes_test(verify_admin_access)
def faculty_detail_view(request, faculty):
    allowed_faculty = [faculty.name.lower() for faculty in Faculty.objects.all()]
    allowed_faculty.append("teacher")

    if faculty not in allowed_faculty:
        raise Http404
    else:
        context = {"faculty": faculty, "semesters": range(1, 9)}
        if faculty == "teacher":
            teachers = Account.objects.filter(faculty="teacher")

            return render(request, "teacher_list.html", {"teachers": teachers})
        return render(request, "faculty_detail.html", context=context)


@login_required
@user_passes_test(verify_admin_access)
def get_students_by_semester(request, faculty, semester):
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
