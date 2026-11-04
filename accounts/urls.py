from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/signup", views.signup, name="signup"),
    path("accounts/registerStudent", views.registerStudent, name="registerStudent"),
    path("students/", views.student_list, name="student_list")
]
