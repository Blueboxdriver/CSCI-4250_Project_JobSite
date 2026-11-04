from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import (
    FacultyProfileForm,
    FacultySignUpForm,
    StudentProfileForm,
    StudentSignUpForm,
)
from .models import Faculty, Student, User


def student_signup(request):
    if request.method == "POST":
        user_form = StudentSignUpForm(request.POST)
        profile_form = StudentProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.role = User.Role.STUDENT
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

            login(request, user)
            return redirect("accounts:student_profile_edit")
    else:
        user_form = StudentSignUpForm()
        profile_form = StudentProfileForm()

    return render(request, "signup.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "student_user_form": user_form,
        "student_profile_form": profile_form,
        "faculty_user_form": FacultySignUpForm(prefix="user"),
        "faculty_profile_form": FacultyProfileForm(prefix="profile"),
        "signup_type": "student",
    })


def faculty_signup(request):
    if request.method == "POST":
        user_form = FacultySignUpForm(request.POST, prefix="user")
        profile_form = FacultyProfileForm(request.POST, prefix="profile")
        if user_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                user = user_form.save(commit=False)
                user.role = User.Role.FACULTY
                user.save()
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()

            login(request, user)
            return redirect("accounts:faculty_pending")
    else:
        user_form = FacultySignUpForm(prefix="user")
        profile_form = FacultyProfileForm(prefix="profile")

    return render(request, "signup.html", {
        "user_form": user_form,
        "profile_form": profile_form,
        "student_user_form": StudentSignUpForm(),
        "student_profile_form": StudentProfileForm(),
        "faculty_user_form": user_form,
        "faculty_profile_form": profile_form,
        "signup_type": "faculty",
    })


@login_required
def faculty_pending(request):
    if request.user.role != User.Role.FACULTY:
        raise PermissionDenied
    profile = Faculty.objects.filter(user=request.user).first()
    if profile and profile.is_approved:
        return redirect("jobs:list")
    return render(request, "faculty_pending.html", status=403)


@login_required
def post_login(request):
    if request.user.role == User.Role.FACULTY:
        faculty = Faculty.objects.filter(user=request.user).first()
        if not faculty or not faculty.is_approved:
            return redirect("accounts:faculty_pending")
    return redirect("jobs:list")


@login_required
@require_http_methods(["GET", "POST"])
def student_profile_edit(request):
    if request.user.role != User.Role.STUDENT:
        raise PermissionDenied
    profile = Student.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("accounts:student_profile_edit")
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, "accounts/student_profile_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def faculty_profile_edit(request):
    _require_approved_faculty(request.user)
    profile = Faculty.objects.filter(user=request.user).first()
    if request.method == "POST":
        form = FacultyProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("accounts:faculty_profile_edit")
    else:
        form = FacultyProfileForm(instance=profile)
    return render(request, "accounts/faculty_profile_form.html", {"form": form})


def _require_approved_faculty(user):
    profile = Faculty.objects.filter(user=user).first()
    if user.role != User.Role.FACULTY or not profile or not profile.is_approved:
        raise PermissionDenied


@login_required
@require_http_methods(["GET"])
def student_list(request):
    _require_approved_faculty(request.user)
    students = (
        Student.objects.filter(
            seeking_employment=True,
            user__role=User.Role.STUDENT,
            user__is_active=True,
        )
        .select_related("user")
        .order_by("user__username")
    )
    return render(request, "accounts/student_list.html", {"students": students})


@login_required
@require_http_methods(["GET"])
def student_detail(request, student_id):
    _require_approved_faculty(request.user)
    student = get_object_or_404(
        Student.objects.select_related("user"),
        pk=student_id,
        seeking_employment=True,
        user__role=User.Role.STUDENT,
        user__is_active=True,
    )
    return render(request, "accounts/student_detail.html", {"student": student})
