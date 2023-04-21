from django.contrib import admin
from .models import Faculty, Subject, Assignment

# Register your models here.
admin.site.register(Subject)
admin.site.register(Faculty)
admin.site.register(Assignment)
