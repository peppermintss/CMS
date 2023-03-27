from django.shortcuts import render
from django.http import Http404
from account.models import Account
from account.models import Account
def faculty_detail_view(request,faculty):
    allowed_faculty = ['csit','bim','teacher']
    if faculty not in allowed_faculty:
       raise Http404
    else:
        context= {
            'faculty': faculty,
            'semesters': range(1,9)
        }
        if faculty == "teacher":
           teachers = Account.objects.filter(faculty='teacher')
           
           return render (request,"teacher_list.html",{'teachers':teachers})
        return render(request,"faculty_detail.html",context=context)


def get_students_by_semester(request,faculty,semester):
   if semester > 8:
    raise Http404
   else:
        students = Account.objects.filter(faculty=faculty).filter(semester=semester)
        context={
            'faculty' : faculty,
            'students':students,
            'semester':semester
        }
        return render(request,"student-by-semester.html",context=context)

