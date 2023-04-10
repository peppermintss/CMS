from django.db import models
from account.models import Account


class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name.lower()


class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)
    faculty = models.ForeignKey(Faculty, to_field="name", on_delete=models.CASCADE)
    teacher = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    semester = models.IntegerField()

    def __str__(self):
        return self.name.lower()
