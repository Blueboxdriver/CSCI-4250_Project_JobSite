from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from accounts.models import User
from .forms import JobPostingForm
from .models import JobPosting


def job_posting_list(request):
    job_postings = JobPosting.objects.select_related("faculty").all()
    return render(request, "jobs/job_posting_list.html", {"job_postings": job_postings})


def job_posting_create(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Sign in before creating a job posting.")
    if request.user.role != User.Role.FACULTY:
        return HttpResponseForbidden("Only faculty users can create job postings.")

    if request.method == "POST":
        form = JobPostingForm(request.POST)
        if form.is_valid():
            posting = form.save(commit=False)
            posting.faculty = request.user
            posting.save()
            return redirect("jobs:list")
    else:
        form = JobPostingForm()

    return render(request, "jobs/job_posting_form.html", {"form": form})
