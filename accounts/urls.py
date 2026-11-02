from django.urls import path

from . import views


# Enables names such as "accounts:student_list" in redirects and templates.
app_name = "accounts"

urlpatterns = [
    # Students create, maintain, and publish their own profile here.
    path(
        "profile/student/",
        views.student_profile_edit,
        name="student_profile_edit",
    ),

    # Faculty create and maintain their own profile here.
    path(
        "profile/faculty/",
        views.faculty_profile_edit,
        name="faculty_profile_edit",
    ),

    # Faculty browse published student profiles.
    path(
        "students/",
        views.student_list,
        name="student_list",
    ),

    # Faculty open a particular published profile.
    # student_id is the Student record's ID, not its linked User ID.
    path(
        "students/<int:student_id>/",
        views.student_detail,
        name="student_detail",
    ),
]