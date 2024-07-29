from django.urls import path

from spotify.views import spotify_login, spotify_callback, spotify_disconnect, PlaylistView, BackupPlaylistsView

urlpatterns = [
    path("callback/", spotify_callback, name="spotify-callback"),
    path("login/", spotify_login, name="spotify-login"),
    path("disconnect/", spotify_disconnect, name="spotify-disconnect"),
    path("playlists/", PlaylistView.as_view(), name="spotify-playlists"),
    path("backup/", BackupPlaylistsView.as_view(), name="spotify-backup"),
]
