from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

#Maybe this model can have a authority field with 1 2 3 values rather than using groups? 

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['username','email','password1','password2',"first_name","last_name","semester","phone_number","address"]