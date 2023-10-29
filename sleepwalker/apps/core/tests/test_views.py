from rest_framework.test import APITestCase, APIClient, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from sleepwalker.apps.authenticate import models


@override_settings(TESTING=True)
class TestViews(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.auth_token = models.AuthToken.objects.create(user=self.user)

        self.client = APIClient()

    def test_health_check(self):
        response = self.client.get(reverse("core:health_check"))

        self.assertEquals(response.status_code, 200)

    def test_auth_check_as_auth(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("core:auth_check"))

        self.assertEquals(response.status_code, 200)

    def test_auth_check_as_not_auth(self):
        response = self.client.get(reverse("core:auth_check"))
        self.assertEquals(response.status_code, 401)

    def test_event_detected_as_auth(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("core:event_detected"))

        self.assertEquals(response.status_code, 204)

    def test_event_detected_as_not_auth(self):
        response = self.client.get(reverse("core:event_detected"))
        self.assertEquals(response.status_code, 401)

    def test_reset_logs_session_not_auth(self):
        response = self.client.post(reverse("core:reset_logs_session"))
        self.assertEquals(response.status_code, 401)

    def test_reset_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.post(reverse("core:reset_logs_session"))

        self.assertEquals(response.status_code, 200)
