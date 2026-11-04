from django.test import Client, TestCase
from django.urls import reverse

from .models import Faculty, Student, User


class AccountFlowTests(TestCase):
    password = "Campus-test-password-475!"

    def student_data(self, **overrides):
        data = {
            "username": "Student@Example.test", "first_name": "Test",
            "last_name": "Student", "password1": self.password,
            "password2": self.password, "student_id": "S100",
            "fields_of_study": "Computer Science", "classification": "junior",
            "level": "undergrad", "credentials": "Python",
            "experience": "Tutoring", "advertisement": "Campus work",
            "seeking_employment": "on",
        }
        data.update(overrides)
        return data

    def test_student_signup_login_and_logout(self):
        response = self.client.post(reverse("accounts:signup"), self.student_data(role="faculty"))
        self.assertRedirects(response, reverse("accounts:student_profile_edit"))
        user = User.objects.get(username="student@example.test")
        self.assertEqual(user.email, user.username)
        self.assertEqual(user.role, User.Role.STUDENT)
        self.assertTrue(user.check_password(self.password))
        self.assertTrue(user.student_profile.seeking_employment)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))
        self.client.post(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("accounts:login"), {
            "username": "STUDENT@EXAMPLE.TEST", "password": self.password,
        })
        self.assertRedirects(response, reverse("accounts:post_login"), fetch_redirect_response=False)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    def test_invalid_registration_creates_no_partial_account(self):
        for invalid in ({"student_id": ""}, {"classification": "invalid"},
                        {"username": "invalid-email"}, {"password2": "different"}):
            with self.subTest(invalid=invalid):
                response = self.client.post(reverse("accounts:signup"), self.student_data(**invalid))
                self.assertEqual(response.status_code, 200)
                self.assertFalse(User.objects.exists())
                self.assertFalse(Student.objects.exists())

    def test_profile_edits_survive_logout_and_password_login(self):
        self.client.post(reverse("accounts:signup"), self.student_data())
        data = self.student_data(credentials="Updated credentials", experience="Updated experience")
        data.pop("seeking_employment")
        self.client.post(reverse("accounts:student_profile_edit"), data)
        self.client.post(reverse("accounts:logout"))
        response = self.client.post(reverse("accounts:login"), {
            "username": "student@example.test", "password": self.password,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("accounts:student_profile_edit"))
        self.assertContains(response, "Updated credentials")
        self.assertContains(response, "Updated experience")
        self.assertFalse(response.context["form"].instance.seeking_employment)

    def test_duplicate_email_and_wrong_password_are_rejected(self):
        self.client.post(reverse("accounts:signup"), self.student_data())
        self.client.logout()
        response = self.client.post(reverse("accounts:signup"), self.student_data(username="STUDENT@example.test"))
        self.assertTrue(response.context["user_form"].errors)
        self.assertEqual(User.objects.count(), 1)
        response = self.client.post(reverse("accounts:login"), {
            "username": "student@example.test", "password": "incorrect",
        })
        self.assertTrue(response.context["form"].errors)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_faculty_registration_requires_admin_approval(self):
        response = self.client.post(reverse("accounts:faculty_signup"), {
            "user-username": "Faculty@Example.test", "user-first_name": "Test",
            "user-last_name": "Faculty", "user-password1": self.password,
            "user-password2": self.password, "profile-faculty_id": "F100",
            "profile-department": "Computing", "profile-title": "Professor",
            "profile-is_approved": "on", "is_staff": "on",
        })
        self.assertRedirects(response, reverse("accounts:faculty_pending"), fetch_redirect_response=False)
        user = User.objects.get(username="faculty@example.test")
        self.assertEqual(user.role, User.Role.FACULTY)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.faculty_profile.is_approved)
        for route in ("accounts:faculty_pending", "accounts:student_list",
                      "accounts:faculty_profile_edit", "jobs:create"):
            self.assertEqual(self.client.get(reverse(route)).status_code, 403)
        admin = User.objects.create_superuser("admin", "admin@example.test", self.password)
        admin_client = Client()
        admin_client.force_login(admin)
        response = admin_client.post(reverse("admin:accounts_faculty_change", args=[user.faculty_profile.pk]), {
            "user": user.pk, "faculty_id": "F100", "department": "Computing",
            "title": "Professor", "is_approved": "on", "_save": "Save",
        })
        self.assertEqual(response.status_code, 302)
        user.faculty_profile.refresh_from_db()
        self.assertTrue(user.faculty_profile.is_approved)
        self.assertRedirects(self.client.get(reverse("accounts:post_login")), reverse("jobs:list"))
        self.assertEqual(self.client.get(reverse("accounts:student_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("jobs:create")).status_code, 200)

        self.client.post(reverse("accounts:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
        response = self.client.post(reverse("accounts:login"), {
            "username": "FACULTY@example.test", "password": self.password,
        }, follow=True)
        self.assertRedirects(response, reverse("jobs:list"))
        self.assertEqual(self.client.get(reverse("accounts:student_list")).status_code, 200)
        self.assertEqual(self.client.get(reverse("jobs:create")).status_code, 200)

    def test_signup_requires_csrf_token(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post(reverse("accounts:signup"), self.student_data()).status_code, 403)
        self.assertFalse(User.objects.exists())

    def test_existing_signup_and_login_pages_supply_working_csrf_tokens(self):
        client = Client(enforce_csrf_checks=True)
        response = client.get(reverse("accounts:signup"))
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        response = client.post(reverse("accounts:signup"), {
            **self.student_data(), "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        })
        self.assertRedirects(response, reverse("accounts:student_profile_edit"))
        client.post(reverse("accounts:logout"), {
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        })
        response = client.get(reverse("accounts:login"))
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        response = client.post(reverse("accounts:login"), {
            "username": "student@example.test", "password": self.password,
            "csrfmiddlewaretoken": client.cookies["csrftoken"].value,
        }, follow=True)
        self.assertRedirects(response, reverse("jobs:list"))


class ProfileAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user("student@example.test", role=User.Role.STUDENT)
        cls.other = User.objects.create_user("other@example.test", role=User.Role.STUDENT)
        cls.profile = Student.objects.create(user=cls.student, student_id="S1", fields_of_study="Computing",
                                            classification="junior", level="undergrad", seeking_employment=True)
        cls.other_profile = Student.objects.create(user=cls.other, fields_of_study="Art", seeking_employment=False)
        cls.faculty = User.objects.create_user("faculty@example.test", role=User.Role.FACULTY)
        cls.faculty_profile = Faculty.objects.create(user=cls.faculty, faculty_id="F1", title="Professor", is_approved=True)

    def test_student_edits_only_own_profile_and_can_toggle_visibility(self):
        self.client.force_login(self.student)
        data = {"student_id": "S1", "fields_of_study": "Mathematics", "classification": "senior",
                "level": "undergrad", "credentials": "Statistics", "experience": "Lab",
                "advertisement": "Research", "user": self.other.pk, "id": self.other_profile.pk}
        self.assertRedirects(self.client.post(reverse("accounts:student_profile_edit"), data), reverse("accounts:student_profile_edit"))
        self.profile.refresh_from_db()
        self.other_profile.refresh_from_db()
        self.assertEqual(self.profile.user, self.student)
        self.assertEqual(self.profile.fields_of_study, "Mathematics")
        self.assertEqual(self.profile.credentials, "Statistics")
        self.assertFalse(self.profile.seeking_employment)
        self.assertEqual(self.other_profile.fields_of_study, "Art")
        self.client.force_login(self.faculty)
        self.assertQuerySetEqual(self.client.get(reverse("accounts:student_list")).context["students"], [])
        self.assertEqual(self.client.get(reverse("accounts:student_detail", args=[self.profile.pk])).status_code, 404)
        self.client.force_login(self.student)
        self.client.post(reverse("accounts:student_profile_edit"), {**data, "seeking_employment": "on"})
        self.client.force_login(self.faculty)
        response = self.client.get(reverse("accounts:student_detail", args=[self.profile.pk]))
        self.assertContains(response, "Seeking employment: Yes")
        self.assertContains(response, "Mathematics")
        self.assertContains(response, "Statistics")

    def test_faculty_browse_excludes_hidden_and_inactive_students(self):
        self.client.force_login(self.faculty)
        response = self.client.get(reverse("accounts:student_list"))
        self.assertEqual(list(response.context["students"]), [self.profile])
        self.assertEqual(self.client.get(reverse("accounts:student_detail", args=[self.other_profile.pk])).status_code, 404)
        self.student.is_active = False
        self.student.save()
        self.assertEqual(self.client.get(reverse("accounts:student_detail", args=[self.profile.pk])).status_code, 404)
        self.assertContains(self.client.get(reverse("accounts:student_list")), "No students have published their profiles yet.")

    def test_profile_access_denied_for_wrong_roles_and_missing_approval(self):
        detail = reverse("accounts:student_detail", args=[self.profile.pk])
        for url in (reverse("accounts:student_profile_edit"), reverse("accounts:student_list"), detail):
            self.assertEqual(self.client.get(url).status_code, 302)
        self.client.force_login(self.student)
        for url in (reverse("accounts:student_list"), detail, reverse("accounts:faculty_profile_edit")):
            self.assertEqual(self.client.get(url).status_code, 403)
        self.client.force_login(self.faculty)
        self.assertEqual(self.client.get(reverse("accounts:student_profile_edit")).status_code, 403)
        self.faculty_profile.is_approved = False
        self.faculty_profile.save()
        for url in (reverse("accounts:student_list"), detail, reverse("accounts:faculty_profile_edit")):
            self.assertEqual(self.client.get(url).status_code, 403)
        self.faculty_profile.delete()
        self.assertEqual(self.client.get(reverse("accounts:student_list")).status_code, 403)

    def test_faculty_edit_preserves_owner_and_approval(self):
        self.client.force_login(self.faculty)
        response = self.client.post(reverse("accounts:faculty_profile_edit"), {
            "faculty_id": "F2", "department": "Mathematics", "title": "Lecturer",
            "user": self.student.pk, "is_approved": "",
        })
        self.assertRedirects(response, reverse("accounts:faculty_profile_edit"))
        self.faculty_profile.refresh_from_db()
        self.assertEqual(self.faculty_profile.user, self.faculty)
        self.assertTrue(self.faculty_profile.is_approved)
        self.assertEqual(self.faculty_profile.department, "Mathematics")

    def test_invalid_profile_edit_preserves_saved_values(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("accounts:student_profile_edit"), {"student_id": ""})
        self.assertTrue(response.context["form"].errors)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.student_id, "S1")
        self.assertTrue(self.profile.seeking_employment)
