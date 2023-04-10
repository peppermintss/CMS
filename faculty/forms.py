from django.forms import ModelForm
from .models import Faculty, Subject


class FacultyAddForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ["name"]


class SubjectAddForm(ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "teacher"]
