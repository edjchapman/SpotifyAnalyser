from django.contrib import admin

from .models import SpotifyToken, Playlist, Track


class TrackInline(admin.TabularInline):
    model = Track
    extra = 1


@admin.register(SpotifyToken)
class SpotifyTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "access_token", "refresh_token", "expires_at")
    search_fields = ("user__username", "access_token", "refresh_token")
    list_filter = ("expires_at",)


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "spotify_id", "public")
    search_fields = ("name", "user__username", "spotify_id")
    list_filter = ("public",)
    inlines = [TrackInline]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("name", "artist", "album", "playlist")
    search_fields = ("name", "artist", "album", "playlist__name")
    list_filter = ("album", "artist", "playlist")
