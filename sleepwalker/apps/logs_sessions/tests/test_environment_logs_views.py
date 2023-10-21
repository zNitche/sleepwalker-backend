from rest_framework.test import APITestCase, APIClient, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from sleepwalker.apps.authenticate.models import AuthToken
from sleepwalker.apps.logs_sessions import models
from sleepwalker.utils import tokens_utils


@override_settings(TESTING=True)
class TestEnvironmentLogsViews(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password,
                                                         api_key=tokens_utils.generate_api_key())
        self.auth_token = AuthToken.objects.create(user=self.user)

        self.client = APIClient()

    def test_environment_sensors_logs_not_auth(self):
        response = self.client.get(reverse("logs_sessions:environment_sensors_logs",
                                           kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_environment_sensors_logs_not_found(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:environment_sensors_logs",
                                           kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 404)

    def test_environment_sensors_logs(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        session = models.LogsSession.objects.create(user=self.user)
        response = self.client.get(reverse("logs_sessions:environment_sensors_logs",
                                           kwargs={"session_uuid": session.uuid}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()), 0)

    def test_add_environment_sensors_logs_not_auth(self):
        response = self.client.post(reverse("logs_sessions:create_environment_sensors_log",
                                            kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_add_environment_sensors_logs_not_found(self):
        self.client.credentials(HTTP_API_KEY=self.user.api_key)
        response = self.client.post(reverse("logs_sessions:create_environment_sensors_log",
                                            kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 404)

    def test_add_environment_sensors_logs(self):
        self.client.credentials(HTTP_API_KEY=self.user.api_key)
        session = models.LogsSession.objects.create(user=self.user)

        log = {
            "temperature": 5,
            "humidity": 1
        }
        response = self.client.post(reverse("logs_sessions:create_environment_sensors_log",
                                            kwargs={"session_uuid": session.uuid}), data=log)

        self.assertEquals(response.status_code, 201)

        logs_session = models.LogsSession.objects.filter(uuid=session.uuid).first()
        self.assertEquals(len(logs_session.environment_sensors_logs.all()), 1)
