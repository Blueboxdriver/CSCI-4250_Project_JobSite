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

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="job_end_Date_on_or_after_start_date",
            )
        ]

    title = models.CharField(max_length=255) #Short name that students can search for
    description = models.TextField() # Description of the job
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True) # Date the posting was created

    # Text Django displays for this posting, such as in the admin.
    def __str__(self):
        return self.title