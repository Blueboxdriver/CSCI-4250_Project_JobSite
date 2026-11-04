from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Faculty, User
from .models import JobPosting


class JobFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user("student@example.test", role=User.Role.STUDENT)
        cls.faculty = User.objects.create_user("faculty@example.test", role=User.Role.FACULTY)
        cls.pending = User.objects.create_user("pending@example.test", role=User.Role.FACULTY)
        cls.missing_profile = User.objects.create_user("missing@example.test", role=User.Role.FACULTY)
        Faculty.objects.create(user=cls.faculty, is_approved=True)
        Faculty.objects.create(user=cls.pending)

    def posting_data(self, **overrides):
        today = timezone.localdate()
        data = {"title": "Campus tutor", "description": "Help students with computing.",
                "start_date": today.isoformat(), "end_date": (today + timedelta(days=30)).isoformat()}
        data.update(overrides)
        return data

    def test_approved_faculty_posts_and_student_reads_saved_job(self):
        self.client.force_login(self.faculty)
        response = self.client.post(reverse("jobs:create"), self.posting_data(faculty=self.pending.pk))
        self.assertRedirects(response, reverse("jobs:list"))
        posting = JobPosting.objects.get()
        self.assertEqual(posting.faculty, self.faculty)
        self.client.force_login(self.student)
        response = self.client.get(reverse("jobs:list"))
        self.assertContains(response, posting.title)
        self.assertContains(response, posting.description)
        self.assertContains(response, self.faculty.username)

    def test_unauthorized_users_cannot_open_or_submit_posting_form(self):
        for user in (None, self.student, self.pending, self.missing_profile):
            with self.subTest(user=user):
                self.client.logout()
                if user:
                    self.client.force_login(user)
                self.assertEqual(self.client.get(reverse("jobs:create")).status_code, 403)
                self.assertEqual(self.client.post(reverse("jobs:create"), self.posting_data()).status_code, 403)
                self.assertFalse(JobPosting.objects.exists())

    def test_invalid_posting_does_not_persist(self):
        self.client.force_login(self.faculty)
        for invalid in ({"title": ""}, {"description": ""}, {"start_date": "invalid"},
                        {"start_date": "2026-02-02", "end_date": "2026-02-01"}):
            with self.subTest(invalid=invalid):
                response = self.client.post(reverse("jobs:create"), self.posting_data(**invalid))
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].errors)
                self.assertFalse(JobPosting.objects.exists())

    def test_browsing_includes_past_current_and_future_postings(self):
        today = timezone.localdate()
        for title, offset in (("Past", -60), ("Current", 0), ("Future", 60)):
            JobPosting.objects.create(faculty=self.faculty, title=title, description=title,
                                      start_date=today + timedelta(days=offset),
                                      end_date=today + timedelta(days=offset + 30))
        self.client.force_login(self.student)
        response = self.client.get(reverse("jobs:list"))
        self.assertEqual(set(response.context["job_postings"].values_list("title", flat=True)), {"Past", "Current", "Future"})
        for title in ("Past", "Current", "Future"):
            self.assertContains(response, title)

    def test_browsing_requires_login_and_handles_empty_database(self):
        response = self.client.get(reverse("jobs:list"))
        self.assertRedirects(response, reverse("accounts:login") + "?next=" + reverse("jobs:list"))
        self.client.force_login(self.student)
        self.assertContains(self.client.get(reverse("jobs:list")), "There are no job postings yet.")

    def test_posting_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.faculty)
        self.assertEqual(client.post(reverse("jobs:create"), self.posting_data()).status_code, 403)
        self.assertFalse(JobPosting.objects.exists())
