from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from spotify.models import SpotifyToken


class SpotifyTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(
            username="testuser", password="password123", email="testuser@example.com"
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
            "expires_at": 3600,
        }

        # Mocking the current user response from Spotify
        mock_current_user.return_value = {"id": "mock_spotify_user_id", "display_name": "Mock Spotify User"}

        response = self.client.get(reverse("spotify-callback"), {"code": "testcode"})
        self.assertEqual(response.status_code, 302)  # Should redirect to profile page

        spotify_token = SpotifyToken.objects.get(user=self.test_user)
        self.assertEqual(spotify_token.access_token, "mock_access_token")
        self.assertEqual(spotify_token.refresh_token, "mock_refresh_token")

    def test_spotify_disconnect_view(self):
        SpotifyToken.objects.create(
            user=self.test_user,
            access_token="testaccesstoken",
            refresh_token="testrefreshtoken",
            expires_at="2025-01-01 00:00:00",
        )
        response = self.client.get(reverse("spotify-disconnect"))
        self.assertEqual(response.status_code, 302)  # Redirect after disconnect
        self.assertFalse(SpotifyToken.objects.filter(user=self.test_user).exists())
