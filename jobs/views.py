from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.models import User
from .forms import JobPostingForm
from .models import JobPosting


@login_required
def job_posting_list(request):
    job_postings = JobPosting.objects.select_related("faculty").all()
    return render(request, "postings.html", {"job_postings": job_postings})


def job_posting_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Sign in before creating a job posting.")
    if request.user.role != User.Role.FACULTY:
        return HttpResponseForbidden("Only faculty users can create job postings.")
    faculty_profile = getattr(request.user, "faculty_profile", None)
    if not faculty_profile or not faculty_profile.is_approved:
        return HttpResponseForbidden("Faculty access requires administrator approval.")

    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.faculty = request.user
            posting.save()
            return redirect("jobs:list")
    else:
        form = JobPostingForm()

    return render(request, "job_posting_form.html", {"form": form})
