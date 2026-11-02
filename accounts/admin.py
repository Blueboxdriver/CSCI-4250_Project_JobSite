from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student


@admin.register(User)
class CampusUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Campus Role", {"fields": ("role",)}),
    )


admin.site.register(Student)
# Register your models here.
