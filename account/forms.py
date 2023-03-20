from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username','email','password1','password2',"first_name","last_name","semester","phone_number"]