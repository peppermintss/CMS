from django.shortcuts import render
from django.http import Http404
from account.models import Account
from .forms import FacultyAddForm
from .models import Faculty
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
    if semester > 8 or faculty not in allowed_faculty:
        raise Http404
    else:
        students = Account.objects.filter(faculty=faculty).filter(semester=semester)
        context = {"faculty": faculty, "students": students, "semester": semester}
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
