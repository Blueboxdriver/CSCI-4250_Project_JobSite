from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        FACULTY = "faculty", "Faculty"

    role = models.CharField(
        max_length=7,
        choices=Role.choices,
        default=Role.STUDENT
    )


class Student(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    student_id = models.CharField(max_length=30, default="")
    email_address = models.CharField(max_length=100, default="")
    fields_of_study = models.CharField(max_length=100, default="")
    
    seeking_employment = models.BooleanField(default=False)

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

class Faculty(models.Model):
    user = models.OneToOneField(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="faculty_profile"
    )

    first_name = models.CharField(max_length=100, default="")
    last_name = models.CharField(max_length=100, default="")
    faculty_id = models.CharField(max_length=30, default="")
    email_address = models.CharField(max_length=100, default="")
    department = models.CharField(max_length=100, default="")
    position = models.CharField(
        max_length=19,
        choices=[
            ("dean", "Dean"),
            ("professor", "Professor"),
            ("associate professor", "Associate Professor"),
        ],
    )
    
    def __str__(self):
        return self.user.username
# Create your models here.
