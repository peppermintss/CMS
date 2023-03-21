from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

#This model probably needs more data that you have forgotten. Just remembered and added 1 hello? Make sure to 
#update admin.py if u chage things here

class Account(AbstractUser):
    address = models.CharField(max_length=150,null=True,blank=True)
    semester = models.IntegerField(null=True,blank=True)
    phone_number = PhoneNumberField(blank=True)
    
    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username