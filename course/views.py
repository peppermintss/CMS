from django.shortcuts import render,HttpResponse

from account.models import Account
def course_detail_view(request,course):
    context= {
        'course': course,
        'semesters': range(1,9)
    }
    
    return render(request,"course_detail.html",context=context)


def get_students_by_semester(request,course,semester):
   
    students = Account.objects.filter(faculty=course).filter(semester=semester)
    context={
        'faculty' : course,
        'students':students,
        'semester':semester
    }
    return render(request,"student-by-semester.html",context=context)

