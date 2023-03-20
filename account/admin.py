from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info',{'fields': ('first_name','last_name','email','semester')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(Account,UserAdmin)