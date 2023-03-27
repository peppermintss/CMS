from django.shortcuts import render
from django.http import Http404

from account.models import Account
def course_detail_view(request,course):
    allowed_courses = ['csit','bim','teacher']
    if course not in allowed_courses:
       raise Http404
    else:
        context= {
            'course': course,
            'semesters': range(1,9)
        }
        
        return render(request,"course_detail.html",context=context)


def get_students_by_semester(request,course,semester):
   if semester > 8:
    raise Http404
   else:
        students = Account.objects.filter(faculty=course).filter(semester=semester)
        context={
            'faculty' : course,
            'students':students,
            'semester':semester
        }
        return render(request,"student-by-semester.html",context=context)

