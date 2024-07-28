from django.conf import settings
from django.db import models

from core.models import BaseModel


class SpotifyToken(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class Playlist(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Track(BaseModel):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    spotify_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255)

    def __str__(self):
        return self.name
