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
    seeking_employment = models.BooleanField(default=False)

    fields_of_study = models.CharField(max_length=500)

    classification = models.CharField(
        max_length=10,
        choices=[
            ("freshman", "Freshman"),
            ("sophomore", "Sophomore"),
            ("junior", "Junior"),
            ("senior", "Senior"),
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
# Create your models here.
