from django.shortcuts import render


# Create your views here.
def home_page(request):
    return render(request,"index.html")

def student_info(request):
    return render(request,"student_info.html")