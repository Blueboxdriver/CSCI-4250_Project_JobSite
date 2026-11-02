from datetime import timedelta

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from accounts.models import Student, User
from jobs.models import JobPosting


class Command(BaseCommand):
    help = "Create fictional, non-loginable student/faculty/job data for local development."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Refusing to create sample data unless DEBUG=True.")

        faculty = self.get_demo_user(
            username="demo_faculty",
            email="demo.faculty@example.test",
            role=User.Role.FACULTY,
            first_name="Demo",
            last_name="Faculty",
        )
        student = self.get_demo_user(
            username="demo_student",
            email="demo.student@example.test",
            role=User.Role.STUDENT,
            first_name="Demo",
            last_name="Student",
        )

        Student.objects.get_or_create(
            user=student,
            defaults={
                "seeking_employment": True,
                "fields_of_study": "Computer Science",
                "classification": "junior",
                "level": "undergrad",
            },
        )

        today = timezone.localdate()
        JobPosting.objects.get_or_create(
            faculty=faculty,
            title="[DEMO] Campus Research Assistant",
            defaults={
                "description": (
                    "[DEMO DATA] Assist with a fictional campus research project. "
                    "This posting is for local development only."
                ),
                "start_date": today + timedelta(days=14),
                "end_date": today + timedelta(days=74),
            },
        )

        self.stdout.write(self.style.SUCCESS(
            "Sample data is ready: demo_faculty, demo_student, one student profile, "
            "and one job posting. These users have unusable passwords."
        ))

    def get_demo_user(self, *, username, email, role, first_name, last_name):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "role": role,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        if not created and (user.email != email or user.role != role):
            raise CommandError(
                f"{username} already exists with different account details; "
                "refusing to change it."
            )
        if created:
            user.set_unusable_password()
            user.save(update_fields=["password"])
        return user
