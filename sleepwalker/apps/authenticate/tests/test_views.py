from rest_framework.test import APITestCase, APIClient, override_settings
from django.contrib.auth import get_user_model
from sleepwalker.apps.authenticate import models


@override_settings(TESTING=True)
class TestViews(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.auth_token = models.AuthToken.objects.create(user=self.user)

        self.client = APIClient()

    def test_login(self):
        response = self.client.post("/api/auth/login/", {
            "username": self.username,
            "password": self.password
        })

        self.assertEquals(response.status_code, 200)
        self.assertIsNot(response.json().get("token"), None)

    def test_logout_auth(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.post("/api/auth/logout/")

        self.assertEquals(response.status_code, 200)

        auth_token = models.AuthToken.objects.filter(key=self.auth_token.key).first()
        self.assertFalse(auth_token.is_valid())

    def test_logout_not_auth(self):
        response = self.client.post("/api/auth/logout/")
        self.assertEquals(response.status_code, 401)

    def test_api_key_creation_auth(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)

        self.assertIs(self.user.api_key, None)
        response = self.client.post("/api/auth/api-key/")

        user = get_user_model().objects.filter(username=self.username).first()

        self.assertEquals(response.status_code, 200)
        self.assertIsNot(user.api_key, None)
        self.assertIsNot(response.json().get("api_key"), None)

    def test_api_key_creation_not_auth(self):
        response = self.client.post("/api/auth/api-key/")
        self.assertEquals(response.status_code, 401)
