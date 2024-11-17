from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword"
        self.user = User.objects.create_user(username=self.username, password=self.password, role="customer")
        self.token_url = "/api/token/"
        self.refresh_url = "/api/token/refresh/"

    def test_login_valid_credentials(self):
        response = self.client.post(self.token_url, {"username": self.username, "password": self.password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid_credentials(self):
        response = self.client.post(self.token_url, {"username": self.username, "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        response = self.client.post(self.token_url, {"username": self.username, "password": self.password})
        refresh_token = response.data["refresh"]
        response = self.client.post(self.refresh_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
