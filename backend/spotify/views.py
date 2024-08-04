from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone as tz
from django.views import View
from spotipy import SpotifyOAuth, Spotify

from spotify.models import SpotifyToken, Playlist, Track
from spotify.services import SpotifyService


class SpotifyLoginView(LoginRequiredMixin, View):
    """
    Initiates Spotify OAuth2 login.
    """

    def get(self, request, *args, **kwargs):
        auth_url = self._get_spotify_oauth().get_authorize_url()
        return redirect(auth_url)

    @staticmethod
    def _get_spotify_oauth():
        """
        Helper function to get SpotifyOAuth instance.
        """
        return SpotifyOAuth(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIPY_REDIRECT_URI,
            scope="user-library-read playlist-read-private",
        )


class SpotifyCallbackView(View):
    """
    Handles Spotify OAuth2 callback.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponse("Unauthorized", status=401)

        token_info = self._get_spotify_tokens(request)
        if token_info:
            self._save_spotify_tokens(request.user, token_info)
            return redirect("profile")
        else:
            return HttpResponse("Error during Spotify authentication")

    @staticmethod
    def _get_spotify_tokens(request):
        """
        Helper function to get Spotify tokens.
        """
        sp_oauth = SpotifyOAuth(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIPY_REDIRECT_URI,
            scope="user-library-read playlist-read-private",
        )
        code = request.GET.get("code")
        return sp_oauth.get_access_token(code)

    @staticmethod
    def _save_spotify_tokens(user, token_info):
        """
        Helper function to save Spotify tokens to the database.
        """
        expires_at = tz.now() + tz.timedelta(seconds=token_info["expires_in"])
        spotify_token, created = SpotifyToken.objects.get_or_create(user=user)
        spotify_token.access_token = token_info["access_token"]
        spotify_token.refresh_token = token_info["refresh_token"]
        spotify_token.expires_at = expires_at
        spotify_token.save()

        # Fetch and save Spotify user ID
        sp = Spotify(auth=spotify_token.access_token)
        spotify_user = sp.current_user()
        user.spotify_id = spotify_user["id"]
        user.save()


class SpotifyDisconnectView(LoginRequiredMixin, View):
    """
    Handles disconnection of Spotify account.
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        try:
            spotify_token = SpotifyToken.objects.get(user=request.user)
            spotify_token.delete()
        except SpotifyToken.DoesNotExist:
            pass
        return redirect("profile")


class BackupPlaylistsView(LoginRequiredMixin, View):
    """
    Backs up the user’s Spotify playlists.
    """

    # noinspection PyMethodMayBeStatic
    def get(self, request, *args, **kwargs):
        spotify_service = SpotifyService(request.user)
        spotify_service.backup_playlists()
        return redirect("spotify-playlists")


class RefreshPlaylistView(LoginRequiredMixin, View):
    # noinspection PyMethodMayBeStatic
    def get(self, request, pk, *args, **kwargs):
        spotify_service = SpotifyService(request.user)
        spotify_service.refresh_playlist(pk)  # Use the primary key directly
        return redirect(reverse("spotify-playlist-detail", args=[pk]))


class PlaylistView(LoginRequiredMixin, View):
    """
    Displays the user’s Spotify playlists.
    """

    template_name = "spotify/playlists.html"

    def get(self, request, *args, **kwargs):
        playlists = Playlist.objects.filter(user=request.user)
        return render(request, self.template_name, {"playlists": playlists})


class PlaylistDetailView(LoginRequiredMixin, View):
    """
    Displays the tracks in a specific Spotify playlist.
    """

    template_name = "spotify/playlist_detail.html"

    def get(self, request, pk, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        tracks = Track.objects.filter(playlist=playlist)
        return render(request, self.template_name, {"playlist": playlist, "tracks": tracks})
