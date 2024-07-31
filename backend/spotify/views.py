from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone as tz
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from spotipy import SpotifyOAuth, Spotify

from spotify.models import SpotifyToken, Playlist, Track
from spotify.services import SpotifyService


@login_required
def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read playlist-read-private",
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@csrf_exempt
def spotify_callback(request):
    if request.user.is_anonymous:
        return HttpResponse("Unauthorized", status=401)

    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIPY_CLIENT_ID,
        client_secret=settings.SPOTIPY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIPY_REDIRECT_URI,
        scope="user-library-read playlist-read-private",
    )

    code = request.GET.get("code")
    token_info = sp_oauth.get_access_token(code)

    if token_info and "access_token" in token_info and "refresh_token" in token_info and "expires_at" in token_info:
        user = request.user
        expires_at = tz.now() + tz.timedelta(seconds=token_info["expires_at"])

        spotify_token, created = SpotifyToken.objects.get_or_create(user=user)
        spotify_token.access_token = token_info["access_token"]
        spotify_token.refresh_token = token_info["refresh_token"]
        spotify_token.expires_at = expires_at
        spotify_token.save()

        # Fetch Spotify user ID and update the User model
        sp = Spotify(auth=token_info["access_token"])
        spotify_user = sp.current_user()
        user.spotify_id = spotify_user["id"]
        user.save()

        return redirect("profile")
    else:
        return HttpResponse("Error during Spotify authentication")


@login_required
def spotify_disconnect(request):
    try:
        spotify_token = SpotifyToken.objects.get(user=request.user)
        spotify_token.delete()
    except SpotifyToken.DoesNotExist:
        pass
    return redirect("profile")


@method_decorator(login_required, name="dispatch")
class BackupPlaylistsView(View):
    def get(self, request, *args, **kwargs):
        spotify_service = SpotifyService(request.user)
        spotify_service.backup_playlists()
        return redirect("spotify-playlists")


@method_decorator(login_required, name="dispatch")
class PlaylistView(View):
    template_name = "spotify/playlists.html"

    def get(self, request, *args, **kwargs):
        playlists = Playlist.objects.filter(user=request.user)
        return render(request, self.template_name, {"playlists": playlists})


@method_decorator(login_required, name="dispatch")
class PlaylistDetailView(View):
    template_name = "spotify/playlist_detail.html"

    def get(self, request, pk, *args, **kwargs):
        playlist = get_object_or_404(Playlist, pk=pk, user=request.user)
        tracks = Track.objects.filter(playlist=playlist)
        return render(request, self.template_name, {"playlist": playlist, "tracks": tracks})
