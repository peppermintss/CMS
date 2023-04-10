from django.forms import ModelForm
from .models import Faculty


class FacultyAddForm(ModelForm):
    class Meta:
        model = Faculty
        fields = ["name"]
