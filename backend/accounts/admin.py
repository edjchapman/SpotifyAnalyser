from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Model Admin
    """

    model = User
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "spotify_id"]
