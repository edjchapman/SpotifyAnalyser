from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountsTests(TestCase):
    def setUp(self):
        self.user_model = get_user_model()
        self.test_user = self.user_model.objects.create_user(
            username="testuser", password="password123", email="testuser@example.com"
        )

    def test_register_view(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_login_view(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_profile_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_user_registration(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "password1": "passbanana1x3",
                "password2": "passbanana1x3",
                "email": "newuser@example.com",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        new_user = self.user_model.objects.get(username="newuser")
        self.assertEqual(new_user.email, "newuser@example.com")
