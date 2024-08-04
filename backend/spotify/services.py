import logging

import spotipy
from django.conf import settings
from django.utils import timezone as tz
from spotipy.oauth2 import SpotifyOAuth

from spotify.models import Playlist, Track

logger = logging.getLogger(__name__)


class SpotifyService:
    def __init__(self, user):
        self.user = user
        self.sp_oauth = SpotifyOAuth(
            client_id=settings.SPOTIPY_CLIENT_ID,
            client_secret=settings.SPOTIPY_CLIENT_SECRET,
            redirect_uri=settings.SPOTIPY_REDIRECT_URI,
            scope="user-library-read playlist-read-private",
        )
        self.sp = self.get_spotify_client()

    def get_spotify_client(self):
        token_info = {
            "access_token": self.user.spotifytoken.access_token,
            "refresh_token": self.user.spotifytoken.refresh_token,
            "expires_at": self.user.spotifytoken.expires_at.timestamp(),
        }
        if self.sp_oauth.is_token_expired(token_info):
            token_info = self.sp_oauth.refresh_access_token(token_info["refresh_token"])
            self._save_spotify_tokens(token_info)
        return spotipy.Spotify(auth=token_info["access_token"])

    def _save_spotify_tokens(self, token_info):
        spotify_token = self.user.spotifytoken
        spotify_token.access_token = token_info["access_token"]
        spotify_token.refresh_token = token_info.get("refresh_token", spotify_token.refresh_token)
        spotify_token.expires_at = tz.now() + tz.timedelta(seconds=token_info["expires_in"])
        spotify_token.save()

    def backup_playlists(self):
        """Backup all playlists for the user."""
        results = self.sp.current_user_playlists()
        while results:
            for item in results["items"]:
                playlist, created = Playlist.objects.update_or_create(
                    spotify_id=item["id"],
                    user=self.user,
                    defaults={
                        "name": item["name"],
                        "description": item.get("description", ""),
                        "public": item["public"],
                    },
                )
                self._update_tracks_for_playlist(playlist)

            # Check if there’s a next page of results
            if results.get("next"):
                results = self.sp.next(results)
            else:
                break

    def refresh_playlist(self, playlist_id):
        """Refresh the tracks of a specific playlist."""
        try:
            playlist = Playlist.objects.get(spotify_id=playlist_id, user=self.user)
            self._update_tracks_for_playlist(playlist)
        except Playlist.DoesNotExist:
            logger.error(f"Playlist with ID {playlist_id} does not exist for the user.")
            return

    def _update_tracks_for_playlist(self, playlist):
        """Fetch and update tracks for a given playlist."""
        existing_track_ids = set(playlist.track_set.values_list("spotify_id", flat=True))
        new_track_ids = set()

        results = self.sp.playlist_items(playlist.spotify_id)
        while results:
            for item in results["items"]:
                try:
                    track = item["track"]
                    new_track, created = Track.objects.update_or_create(
                        playlist=playlist,
                        spotify_id=track["id"],
                        defaults={
                            "name": track["name"],
                            "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                            "album": track["album"]["name"],
                        },
                    )
                    new_track_ids.add(new_track.spotify_id)
                except Exception as e:
                    logger.exception(f"Error fetching track: {e}")
            results = self.sp.next(results)

        # Remove tracks that are no longer in the playlist
        to_delete = existing_track_ids - new_track_ids
        if to_delete:
            Track.objects.filter(playlist=playlist, spotify_id__in=to_delete).delete()
