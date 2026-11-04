from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import EmailAuthenticationForm

app_name = "accounts"

urlpatterns = [
    path("signup/", views.student_signup, name="signup"),
    path("signup/faculty/", views.faculty_signup, name="faculty_signup"),
    path("faculty/pending/", views.faculty_pending, name="faculty_pending"),
    path("post-login/", views.post_login, name="post_login"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            authentication_form=EmailAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path("profile/student/", views.student_profile_edit, name="student_profile_edit"),
    path("profile/faculty/", views.faculty_profile_edit, name="faculty_profile_edit"),
    path("students/", views.student_list, name="student_list"),
    path("students/<int:student_id>/", views.student_detail, name="student_detail"),
]
