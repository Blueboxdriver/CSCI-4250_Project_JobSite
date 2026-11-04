from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_alter_user_role_student_delete_studentprofile"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="student_id",
            field=models.CharField(blank=True, default="", max_length=30),
        ),
        migrations.AddField(
            model_name="student",
            name="credentials",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="student",
            name="experience",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="student",
            name="advertisement",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="student",
            name="classification",
            field=models.CharField(
                choices=[
                    ("freshman", "Freshman"),
                    ("sophomore", "Sophomore"),
                    ("junior", "Junior"),
                    ("senior", "Senior"),
                    ("graduate", "Graduate"),
                ],
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Faculty",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("faculty_id", models.CharField(blank=True, default="", max_length=30)),
                ("department", models.CharField(blank=True, default="", max_length=100)),
                ("title", models.CharField(blank=True, default="", max_length=100)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="faculty_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
