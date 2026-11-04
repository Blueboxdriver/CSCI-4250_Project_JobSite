from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Faculty, Student, User


@admin.register(User)
class CampusUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Campus Role", {"fields": ("role",)}),
    )


admin.site.register(Student)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("user", "faculty_id", "department", "title", "is_approved")
    list_filter = ("is_approved",)
    list_editable = ("is_approved",)
