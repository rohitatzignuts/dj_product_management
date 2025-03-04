from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse


class AuthenticationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.login_url = reverse("jwt-create")
        self.refresh_url = reverse("jwt-refresh")
        self.logout_url = reverse("token_logout")
        self.register_url = reverse("user-list")

    def get_user_tokens(self):
        refresh = RefreshToken.for_user(self.user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    def test_user_registration(self):
        data = {
            "username": "newuser",
            "password": "test@123",
            "email": "newuser@faker.com",
            "first_name": "newuser",
            "last_name": "Golberg",
        }

        response = self.client.post(self.register_url, data)
        # print(response.status_code, response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        data = {"username": "testuser", "password": "password"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        token = self.get_user_tokens()
        data = {"refresh": token["refresh"]}
        response = self.client.post(self.refresh_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_logout(self):
        token = self.get_user_tokens()
        self.client.credentials(HTTP_AUTHORIZATION=f"JWT {token['access']}")
        data = {"refresh": token["refresh"]}
        response = self.client.post(self.logout_url, data)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
