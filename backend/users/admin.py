from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom User Model Admin
    """

    model = User
    list_display = ["username", "email", "first_name", "last_name", "is_staff", "spotify_id"]
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("spotify_id", "access_token", "refresh_token", "token_expiry")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("spotify_id", "access_token", "refresh_token", "token_expiry")}),
    )
