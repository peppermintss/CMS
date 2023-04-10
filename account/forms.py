from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account

# Maybe this model can have a authority field with 1 2 3 values rather than using groups?


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields["password1"].required = False
        self.fields["password2"].required = False

        self.fields["password1"].widget.attrs["autocomplete"] = "off"
        self.fields["password2"].widget.attrs["autocomplete"] = "off"

    class Meta:
        model = Account
        fields = [
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
            "phone_number",
            "address",
        ]
