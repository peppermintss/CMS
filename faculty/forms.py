from django.forms import ModelForm, widgets
from .models import Faculty, Subject, Assignment


class FacultyAddForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ["name"]


class SubjectAddForm(ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "teacher"]


class AssignmentAddForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ["title", "start_date", "deadline", "assignment_file"]
        widgets = {
            "start_date": widgets.DateInput(attrs={"type": "date"}),
            "deadline": widgets.DateInput(attrs={"type": "date"}),
        }
