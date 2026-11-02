from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import StudentProfileForm, FacultyProfileForm
from .models import Student, Faculty, User


# If the visitor is not logged in, redirect them to the login page.
@login_required

# This view accepts opening the page (GET) and submitting its form (POST).
@require_http_methods(["GET", "POST"])
def student_profile_edit(request):
    """Create or update the signed-in student's own profile."""

    # request.user is the account currently signed in.
    # A faculty account must not be allowed to edit a student profile.
    if request.user.role != User.Role.STUDENT:
        raise PermissionDenied  # Return an HTTP 403 Forbidden response.

    # Look for a Student profile belonging to the signed-in account
    # first() returns the profile if found, or None if none exists.
    profile = Student.objects.filter(user=request.user).first()

    if request.method == "POST":
        # POST means the browser submitted the form
        # request.POST contains the submitted field values
        #
        # instance=profile tells the form which database record to update.
        # If profile is None, the form prepares a new Student record.
        form = StudentProfileForm(request.POST, instance=profile)

        # Validate the submitted values using the form's rules.
        # For example, classification must be one of the allowed choices.
        if form.is_valid():
            # Build/update the Student object without saving it yet.
            # This lets us assign its owner before writing to the database.
            profile = form.save(commit=False)

            # Link the profile to the signed-in account.
            # The student cannot select or change the profile's owner.
            profile.user = request.user

            # Write the profile to the database.
            profile.save()

            # Send the browser back to the profile editing page.
            # Redirecting prevents a refresh from repeating the POST.
            # This name must match a named route in accounts/urls.py.
            return redirect("accounts:student_profile_edit")

    else:
        # GET means the visitor opened the page without submitting changes.
        # Display existing profile values, or a blank form for a new profile.
        form = StudentProfileForm(instance=profile)

    # Display the HTML template and give it the form.
    # The template accesses it using the variable name "form".
    #
    # Invalid POST submissions also reach this line. In that case, the form
    # contains the submitted values and validation errors for display.
    return render(
        request,
        "accounts/student_profile_form.html",
        {"form": form},
    )


@login_required
@require_http_methods(["GET", "POST"])
def faculty_profile_edit(request):
    """Create or update the signed-in faculty member's own profile."""

    # Only faculty accounts may use this page.
    if request.user.role != User.Role.FACULTY:
        raise PermissionDenied

    # Find this faculty member's profile, or None if it does not exist.
    profile = Faculty.objects.filter(user=request.user).first()

    if request.method == "POST":
        # Fill the form with submitted values.
        # Passing an existing profile makes this an update instead of
        # creating a second profile for the same account.
        form = FacultyProfileForm(request.POST, instance=profile)

        if form.is_valid():
            # Delay saving until the account relationship has been assigned.
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Return to the editing page after a successful save.
            return redirect("accounts:faculty_profile_edit")

    else:
        # Show current position and department, or an empty form.
        form = FacultyProfileForm(instance=profile)

    # Show the form on the initial visit or after an invalid submission.
    return render(
        request,
        "accounts/faculty_profile_form.html",
        {"form": form},
    )


@login_required
# This page displays information; it does not accept form submissions.
@require_http_methods(["GET"])
def student_list(request):
    """Show faculty the students who published their employment profiles."""

    # Signing in as a student does not grant access to this faculty page.
    if request.user.role != User.Role.FACULTY:
        raise PermissionDenied

    students = (
        Student.objects
        .filter(
            # Show only profiles whose owners chose to advertise.
            seeking_employment=True,

            # The double underscore follows the relationship to User.
            # This checks the role field on the linked account.
            user__role=User.Role.STUDENT,

            # Exclude profiles belonging to disabled accounts.
            user__is_active=True,
        )
        # Retrieve linked User information in the same database query.
        # This avoids an extra query for each student's username/name.
        .select_related("user")

        # Sort the results alphabetically by the linked user's username.
        .order_by("user__username")
    )

    # Give the template the collection under the name "students".
    # The template can loop through it to display each profile.
    return render(
        request,
        "accounts/student_list.html",
        {"students": students},
    )


@login_required
@require_http_methods(["GET"])
def student_detail(request, student_id):
    """Show faculty one published student profile."""

    # Only faculty may open this page.
    if request.user.role != User.Role.FACULTY:
        raise PermissionDenied

    # student_id comes from the URL:
    # students/<int:student_id>/
    #
    # pk means primary key: here, the Student record's automatically
    # generated ID. It is not necessarily the linked User's ID.
    #
    # Apply the same publication rules used by student_list.
    # Otherwise, someone could access an unpublished profile by its URL.
    #
    # If no matching published profile exists, return HTTP 404 Not Found.
    student = get_object_or_404(
        Student.objects.select_related("user"),
        pk=student_id,
        seeking_employment=True,
        user__role=User.Role.STUDENT,
        user__is_active=True,
    )

    # Give the template this single profile under the name "student".
    return render(
        request,
        "accounts/student_detail.html",
        {"student": student},
    )