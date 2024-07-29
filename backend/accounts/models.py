from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    Custom user model that extends the default Django user model.
    Adds additional fields for Spotify integration.
    """

    spotify_id = models.CharField(max_length=50, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username
