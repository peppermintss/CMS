from django.shortcuts import render

def course_detail_view(request,course):
    context= {
        'course': course
    }
    return render(request,"course_detail.html",context=context)