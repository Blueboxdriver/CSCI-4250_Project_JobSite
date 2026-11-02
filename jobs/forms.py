from django import forms

from .models import JobPosting


class JobPostingForm(forms.ModelForm):
    """Form for faculty to create postings; ownership is assigned by the view."""

    class Meta:
        model = JobPosting
        fields = ("title", "description", "start_date", "end_date")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
