from django.db import models
from account.models import Account


def file_name_generator(instance, filename):
    return f"{instance.subject}_assignment"


class Faculty(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name.lower()


class Subject(models.Model):
    name = models.CharField(max_length=30, unique=True)
    faculty = models.ForeignKey(Faculty, to_field="name", on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        Account,
        limit_choices_to={"groups__name": "teacher"},
        on_delete=models.DO_NOTHING,
    )
    semester = models.IntegerField()
    notice = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name.lower()


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    start_date = models.DateField()
    deadline = models.DateField()
    assignment_file = models.FileField(upload_to=file_name_generator)
    subject = models.ForeignKey(Subject, on_delete=models.DO_NOTHING, to_field="name")

    def __str__(self):
        return self.title.lower()
