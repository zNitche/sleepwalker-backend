from rest_framework.test import APITestCase, APIClient, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime
from sleepwalker.apps.authenticate.models import AuthToken
from sleepwalker.apps.logs_sessions import models
from sleepwalker.utils import tokens_utils


@override_settings(TESTING=True)
class TestLogsSessionsViews(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password,
                                                         api_key=tokens_utils.generate_api_key())
        self.auth_token = AuthToken.objects.create(user=self.user)

        self.client = APIClient()

    def test_logs_sessions_not_auth(self):
        response = self.client.get(reverse("logs_sessions:logs_sessions"))
        self.assertEquals(response.status_code, 401)

    def test_logs_sessions(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:logs_sessions"))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json().get("data")), 0)

    def test_latest_running_logs_session_not_auth(self):
        response = self.client.get(reverse("logs_sessions:latest_running_logs_session"))

        self.assertEquals(response.status_code, 401)

    def test_latest_running_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:latest_running_logs_session"))

        self.assertEquals(response.status_code, 404)

        models.LogsSession.objects.create(user=self.user, end_date=datetime.utcnow())
        unfinished_session = models.LogsSession.objects.create(user=self.user)

        response = self.client.get(reverse("logs_sessions:latest_running_logs_session"))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json().get("uuid"), unfinished_session.uuid)

    def test_init_logs_session_not_auth(self):
        response = self.client.post(reverse("logs_sessions:create_logs_session"))
        self.assertEquals(response.status_code, 401)

    def test_init_logs_session(self):
        self.client.credentials(HTTP_API_KEY=self.user.api_key)
        response = self.client.post(reverse("logs_sessions:create_logs_session"))
        session_uuid = response.json().get("uuid")

        self.assertEquals(response.status_code, 201)
        self.assertIsNot(session_uuid, None)

        session = models.LogsSession.objects.filter(uuid=session_uuid).first()
        self.assertIsNot(session, None)

    def test_init_logs_session_already_existing(self):
        self.client.credentials(HTTP_API_KEY=self.user.api_key)
        self.client.post(reverse("logs_sessions:create_logs_session"))

        response = self.client.post(reverse("logs_sessions:create_logs_session"))

        self.assertEquals(response.status_code, 200)

    def test_logs_sessions_statistics_not_auth(self):
        response = self.client.get(reverse("logs_sessions:logs_sessions_statistics"))
        self.assertEquals(response.status_code, 401)

    def test_logs_sessions_statistics(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:logs_sessions_statistics"))
        self.assertEquals(response.status_code, 200)

    def test_reset_current_logs_session_not_auth(self):
        response = self.client.post(reverse("logs_sessions:reset_current_logs_session"))
        self.assertEquals(response.status_code, 401)

    def test_reset_current_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.post(reverse("logs_sessions:reset_current_logs_session"))

        self.assertEquals(response.status_code, 200)
