from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_posting_list, name="list"),
    path("create/", views.job_posting_create, name="create"),
]
