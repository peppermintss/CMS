from django.db import models
from django.contrib.auth.models import AbstractUser

# This model probably needs more data that you have forgotten. Just remembered and added 1 hello? Make sure to
# update admin.py if u change things here


class Account(AbstractUser):
    address = models.CharField(max_length=150, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10)
    faculty = models.CharField(max_length=50)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


class Attendance(models.Model):
    date = models.DateField()
    students = models.ManyToManyField(
        Account,
        limit_choices_to={"groups__name": "student"},
        related_name="students_present",
        blank=True,
    )

    def __str__(self):
        return str(self.date)
