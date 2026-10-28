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


class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    seeking_employment = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
# Create your models here.
