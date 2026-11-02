from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student, User


class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = (
            "fields_of_study",
            "classification",
            "level",
            "seeking_employment",
        )