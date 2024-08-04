from django.urls import path

from spotify.views import (
    SpotifyLoginView,
    SpotifyCallbackView,
    SpotifyDisconnectView,
    BackupPlaylistsView,
    PlaylistView,
    PlaylistDetailView,
    RefreshPlaylistView,
)

urlpatterns = [
    path("login/", SpotifyLoginView.as_view(), name="spotify-login"),
    path("callback/", SpotifyCallbackView.as_view(), name="spotify-callback"),
    path("disconnect/", SpotifyDisconnectView.as_view(), name="spotify-disconnect"),
    path("playlists/", PlaylistView.as_view(), name="spotify-playlists"),
    path(
        "playlists/<uuid:pk>/",
        PlaylistDetailView.as_view(),
        name="spotify-playlist-detail",
    ),
    path("backup/", BackupPlaylistsView.as_view(), name="spotify-backup"),
    path(
        "playlists/<uuid:pk>/refresh/",
        RefreshPlaylistView.as_view(),
        name="spotify-playlist-refresh",
    ),  # New URL for refreshing a specific playlist
]
