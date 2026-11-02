from django import forms

from .models import Student, Faculty


# Handle student profile form
# This form allows students to create and update their profile information
class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student

        # Only these fields can be submitted through this form.
        # "user" is excluded because the view assigns ownership.
        fields = [
            "fields_of_study",
            "classification",
            "level",
            "credentials",
            "experience",
            "advertisement",
            "seeking_employment",
        ]

        labels = {
            "seeking_employment": "Publish my profile to faculty",
            "advertisement": "Describe the employment you are seeking",
        }

# Handle faculty profile form
# This form allows faculty to create and update their profile information
class FacultyProfileForm(forms.ModelForm):
    class Meta:
        model = Faculty

        # Only these fields can be submitted through this form.
        # "user" is excluded because the view assigns ownership.
        fields = [
            "department",
            "title",
        ]