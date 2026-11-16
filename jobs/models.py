from django.conf import settings
from django.db import models


# One database record represents one job posting.
class JobPosting(models.Model):
    DEPARTMENT_CHOICES = [
        ("Office of International Enrollment and Services",
         "Office of International Enrollment and Services"),
        ("Office of Admissions", "Office of Admissions"),
        ("D.P. Culp Student Center", "D.P. Culp Student Center"),
        ("Housing and Residence Life", "Housing and Residence Life"),
        ("Office of Financial Aid and Scholarships",
         "Office of Financial Aid and Scholarships"),
        ("Center for Academic Achievement",
         "Center for Academic Achievement"),
        ("Sherrod Library", "Sherrod Library"),
        ("Campus Recreation", "Campus Recreation"),
        ("Athletics Department", "Athletics Department"),
        ("Sodexo Dining Services", "Sodexo Dining Services"),
        ("Martin Center for the Arts", "Martin Center for the Arts"),
        ("Reece Museum", "Reece Museum"),
    ]
    
    department = models.CharField(
        max_length=255,
        choices=DEPARTMENT_CHOICES,
        default="Sodexo Dining Services",
    )
    
    # Connects the posting to its faculty user.
    # The admin form will offer users whose role is faculty.
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_postings",
        limit_choices_to={"role": "faculty"},
    )

    title = models.CharField(max_length=255)
    department = models.CharField(
        max_length=100,
        choices=DEPARTMENT_CHOICES,
    )
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_date__gte=models.F("start_date")),
                name="job_end_Date_on_or_after_start_date",
            )
        ]

    # Text Django displays for this posting, such as in the admin.
    def __str__(self):
        return self.department