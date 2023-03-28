from django.db import models
from account.models import Account

class Course(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name.lower()