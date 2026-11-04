from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# for DB
class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        FACULTY = "faculty", "Faculty"

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.STUDENT
    )


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    student_id = models.CharField(max_length=30, blank=True, default="")
    credentials = models.TextField(blank=True, default="")
    experience = models.TextField(blank=True, default="")
    advertisement = models.TextField(blank=True, default="")
    seeking_employment = models.BooleanField(default=False)

    fields_of_study = models.CharField(max_length=500)

    classification = models.CharField(
        max_length=10,
        choices=[
            ("freshman", "Freshman"),
            ("sophomore", "Sophomore"),
            ("junior", "Junior"),
            ("senior", "Senior"),
            ("graduate", "Graduate"),
        ],
    )

    level = models.CharField(
        max_length=12,
        choices=[
            ("undergrad", "Undergraduate"),
            ("grad", "Graduate"),
        ],
    )

    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="faculty_profile",
    )
    faculty_id = models.CharField(max_length=30, blank=True, default="")
    department = models.CharField(max_length=100, blank=True, default="")
    title = models.CharField(max_length=100, blank=True, default="")
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username
# Create your models here.
