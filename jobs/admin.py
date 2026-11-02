from django.contrib import admin

from .models import JobPosting


# Lets the admin create and edit job posting records.
admin.site.register(JobPosting)