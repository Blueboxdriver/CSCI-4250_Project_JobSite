from django.shortcuts import render
from .models import JobPosting

# Create your views here.
def job_posting_list(request):
    job_postings = JobPosting.objects.all()
    return render(request, "jobs/job_posting_list.html", {"job_postings": job_postings})



