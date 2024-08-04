from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone as tz

from spotify.models import SpotifyToken, Playlist
from spotify.services import SpotifyService


class SpotifyTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(
            username="testuser", password="password123", email="testuser@example.com"
        )
        self.spotify_token = SpotifyToken.objects.create(
            user=self.test_user,
            access_token="testaccesstoken",
            refresh_token="testrefreshtoken",
            expires_at=tz.now() + tz.timedelta(hours=1),
        )
        self.client.login(username="testuser", password="password123")

    def test_spotify_login_view(self):
        response = self.client.get(reverse("spotify-login"))
        self.assertEqual(response.status_code, 302)  # Redirect to Spotify auth

    @patch("spotipy.oauth2.SpotifyOAuth.get_access_token")
    @patch("spotipy.client.Spotify.current_user")
    def test_spotify_callback_view(self, mock_current_user, mock_get_access_token):
        # Mocking the access token response from Spotify
        mock_get_access_token.return_value = {
            "access_token": "mock_access_token",
            "refresh_token": "mock_refresh_token",
            "expires_in": 3600,  # Time in seconds until the token expires
        }

        # Mocking the current user response from Spotify
        mock_current_user.return_value = {
            "id": "mock_spotify_user_id",
            "display_name": "Mock Spotify User",
        }

        response = self.client.get(reverse("spotify-callback"), {"code": "testcode"})
        self.assertEqual(response.status_code, 302)  # Should redirect to profile page

        spotify_token = SpotifyToken.objects.get(user=self.test_user)
        self.assertEqual(spotify_token.access_token, "mock_access_token")
        self.assertEqual(spotify_token.refresh_token, "mock_refresh_token")
        self.assertTrue(spotify_token.expires_at > tz.now())  # Ensure expiration is set correctly

    def test_spotify_disconnect_view(self):
        # Ensure any existing token is deleted
        SpotifyToken.objects.filter(user=self.test_user).delete()

        # Create a new token for the test
        SpotifyToken.objects.create(
            user=self.test_user,
            access_token="testaccesstoken",
            refresh_token="testrefreshtoken",
            expires_at=tz.now() + tz.timedelta(hours=1),
        )

        response = self.client.get(reverse("spotify-disconnect"))
        self.assertEqual(response.status_code, 302)  # Redirect after disconnect
        self.assertFalse(SpotifyToken.objects.filter(user=self.test_user).exists())

    @patch("spotipy.client.Spotify.current_user_playlists")
    @patch("spotify.services.SpotifyService.fetch_and_store_tracks")
    def test_backup_playlists(self, mock_fetch_and_store_tracks, mock_current_user_playlists):
        mock_current_user_playlists.return_value = {
            "items": [
                {
                    "id": "playlist1",
                    "name": "Playlist 1",
                    "description": "Description 1",
                    "public": True,
                }
            ]
        }
        service = SpotifyService(self.test_user)
        service.backup_playlists()

        playlists = Playlist.objects.filter(user=self.test_user)
        self.assertEqual(playlists.count(), 1)
        self.assertEqual(playlists[0].spotify_id, "playlist1")
        self.assertEqual(playlists[0].name, "Playlist 1")
        self.assertEqual(playlists[0].description, "Description 1")
        self.assertTrue(playlists[0].public)
        mock_fetch_and_store_tracks.assert_called_once_with(playlists[0])
