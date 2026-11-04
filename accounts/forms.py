from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Faculty, Student, User


class _CampusSignUpForm(UserCreationForm):
    username = forms.EmailField(label="Email address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name")

    def clean_username(self):
        username = super().clean_username().lower()
        if User.objects.filter(email__iexact=username).exists():
            raise forms.ValidationError("An account already uses this email address.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class StudentSignUpForm(_CampusSignUpForm):
    pass


class FacultySignUpForm(_CampusSignUpForm):
    pass


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email address")

    def clean(self):
        self.cleaned_data["username"] = self.cleaned_data.get("username", "").lower()
        return super().clean()


class StudentProfileForm(forms.ModelForm):
    student_id = forms.CharField(max_length=30, label="Student ID")

    class Meta:
        model = Student
        fields = (
            "student_id",
            "fields_of_study",
            "classification",
            "level",
            "credentials",
            "experience",
            "advertisement",
            "seeking_employment",
        )


class FacultyProfileForm(forms.ModelForm):
    faculty_id = forms.CharField(max_length=30, label="Faculty ID")
    title = forms.CharField(max_length=100, label="Position")

    class Meta:
        model = Faculty
        fields = ("faculty_id", "department", "title")
