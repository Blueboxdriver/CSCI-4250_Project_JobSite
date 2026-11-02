from django.conf import settings
from django.db import models


# One database record represents one job posting.
class JobPosting(models.Model):
    # Connects the posting to its faculty user.
    # The admin form will offer users whose role is faculty.
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_postings",
        limit_choices_to={"role": "faculty"},
    )

    # The posting's dates and description.
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    # Text Django displays for this posting, such as in the admin.
    def __str__(self):
        return f"Job posting {self.pk}"