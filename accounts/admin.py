from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, StudentProfile


@admin.register(User)
class CampusUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Campus Role", {"fields": ("role",)}),
    )


admin.site.register(StudentProfile)
# Register your models here.
