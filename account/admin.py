from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Attendance


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info',{'fields': ('first_name','last_name','email','semester','phone_number','faculty')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(Account,UserAdmin)
admin.site.register(Attendance)