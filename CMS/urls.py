"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from account.views import register_page,dashboard,add_account
from django.contrib.auth.views import LoginView, LogoutView
from faculty.views import faculty_detail_view,get_students_by_semester,add_course

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',register_page,name="register-page"),
    path('',LoginView.as_view(template_name="login.html",redirect_authenticated_user= True),name="home-page"),
    path('logout/',LogoutView.as_view(template_name="logout.html"),name="logout-page"),
    path('dashboard/',dashboard,name='dashboard'),
    
    path('<str:faculty>/',faculty_detail_view,name="faculty-detail-view"),
    path('<str:faculty>/<int:semester>/',get_students_by_semester,name="students-by-semester"),
    path('add_account/<str:faculty>/<int:semester>',add_account,name="add-account"),
    path('faculty/add_course/',add_course,name="add-course"),
    path("__reload__/", include("django_browser_reload.urls")),
    
  
]

