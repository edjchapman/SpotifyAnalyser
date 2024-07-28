from django.contrib import admin

from spotify.models import SpotifyToken, Playlist, Track

admin.site.register(SpotifyToken)
admin.site.register(Playlist)
admin.site.register(Track)
