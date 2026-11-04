from django.contrib import admin
from django.urls import include, path
from jobs.views import home

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("jobs/", include("jobs.urls")),
    path("accounts/", include("accounts.urls")),
]
