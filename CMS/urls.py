from django.contrib import admin
from django.urls import path, include
from account.views import register_page, dashboard, add_account
from django.contrib.auth.views import LoginView, LogoutView
from faculty.views import (
    faculty_detail_view,
    get_students_by_semester,
    add_course,
    add_subject,
)
from django.contrib.auth.models import Group


# THIS FILE IS IMPORTED ONLY ONCE WHEN THE SERVER RUNS. SO THIS BLOCK OF CODE WILL RUN ONLY ONCE WHEN THE SERVER IS STARTED. PROBABLY
# NOT THE BEST FIX BUT IT WORKS AS INTENDED.


groups_to_create = ["student", "teacher", "admin"]
for group_name in groups_to_create:
    Group.objects.get_or_create(name=group_name)
print("Done")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", register_page, name="register-page"),
    path(
        "",
        LoginView.as_view(template_name="login.html", redirect_authenticated_user=True),
        name="home-page",
    ),
    path(
        "logout/", LogoutView.as_view(template_name="logout.html"), name="logout-page"
    ),
    path("dashboard/", dashboard, name="dashboard"),
    path("<str:faculty>/", faculty_detail_view, name="faculty-detail-view"),
    path(
        "show/<str:faculty>/<int:semester>/",
        get_students_by_semester,
        name="students-by-semester",
    ),
    path("add_account/<str:faculty>/<int:semester>/", add_account, name="add-account"),
    path("faculty/add_course/", add_course, name="add-course"),
    path(
        "faculty/add_subject/<str:faculty>/<int:semester>",
        add_subject,
        name="add-subject",
    ),
    path("__reload__/", include("django_browser_reload.urls")),
]
