import logging

import spotipy

from spotify.models import Playlist, Track

logger = logging.getLogger(__name__)


class SpotifyService:
    def __init__(self, user):
        self.user = user
        self.sp = spotipy.Spotify(auth=user.spotifytoken.access_token)

    def backup_playlists(self):
        results = self.sp.current_user_playlists()
        for item in results["items"]:
            playlist, created = Playlist.objects.get_or_create(
                spotify_id=item["id"],
                user=self.user,
                defaults={"name": item["name"], "description": item.get("description", ""), "public": item["public"]},
            )
            if created:
                self.fetch_and_store_tracks(playlist)

    def fetch_and_store_tracks(self, playlist):
        results = self.sp.playlist_items(playlist.spotify_id)
        for item in results["items"]:
            try:
                track = item["track"]
                Track.objects.create(
                    playlist=playlist,
                    spotify_id=track["id"],
                    name=track["name"],
                    artist=", ".join([artist["name"] for artist in track["artists"]]),
                    album=track["album"]["name"],
                )
            except Exception as e:
                logger.exception(f"Error fetching track: {e}")
