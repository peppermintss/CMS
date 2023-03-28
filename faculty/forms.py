from django.forms import ModelForm
from .models import Course

class CourseAddForm(ModelForm):
    class Meta:
        model = Course
        fields= ['name']