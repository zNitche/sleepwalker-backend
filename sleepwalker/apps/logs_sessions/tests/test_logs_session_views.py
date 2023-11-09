from rest_framework.test import APITestCase, APIClient, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from sleepwalker.apps.authenticate.models import AuthToken
from sleepwalker.apps.logs_sessions import models
from sleepwalker.utils import tokens_utils


@override_settings(TESTING=True)
class TestLogsSessionViews(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username,
                                                         password=self.password,
                                                         api_key=tokens_utils.generate_api_key())
        self.auth_token = AuthToken.objects.create(user=self.user)

        self.client = APIClient()

    def test_logs_session_not_auth(self):
        response = self.client.get(reverse("logs_sessions:logs_session",
                                           kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_logs_session_not_found(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:logs_session",
                                           kwargs={"session_uuid": "123"}))

        self.assertEquals(response.status_code, 404)

    def test_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        session = models.LogsSession.objects.create(user=self.user)
        response = self.client.get(reverse("logs_sessions:logs_session",
                                           kwargs={"session_uuid": session.uuid}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json().get("uuid"), session.uuid)

    def test_close_logs_session_not_auth(self):
        response = self.client.post(reverse("logs_sessions:close_logs_session",
                                            kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_close_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        session = models.LogsSession.objects.create(user=self.user)
        response = self.client.post(reverse("logs_sessions:close_logs_session",
                                            kwargs={"session_uuid": session.uuid}))

        self.assertEquals(response.status_code, 200)
        closed_session = models.LogsSession.objects.filter(uuid=session.uuid).first()
        self.assertIsNot(closed_session.end_date, None)

    def test_remove_logs_session_not_auth(self):
        response = self.client.delete(reverse("logs_sessions:remove_logs_session",
                                              kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_remove_logs_session(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        session = models.LogsSession.objects.create(user=self.user)
        response = self.client.delete(reverse("logs_sessions:remove_logs_session",
                                              kwargs={"session_uuid": session.uuid}))

        self.assertEquals(response.status_code, 200)
        removed_session = models.LogsSession.objects.filter(uuid=session.uuid).first()
        self.assertIs(removed_session, None)

    def test_sleepwalking_events_not_auth(self):
        response = self.client.get(reverse("logs_sessions:sleepwalking_events",
                                           kwargs={"session_uuid": "123"}))
        self.assertEquals(response.status_code, 401)

    def test_sleepwalking_events_session_not_found(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)
        response = self.client.get(reverse("logs_sessions:sleepwalking_events",
                                           kwargs={"session_uuid": "123"}))

        self.assertEquals(response.status_code, 404)

    def test_sleepwalking_events(self):
        self.client.credentials(HTTP_AUTH_TOKEN=self.auth_token.key)

        session = models.LogsSession.objects.create(user=self.user)
        response = self.client.get(reverse("logs_sessions:sleepwalking_events",
                                           kwargs={"session_uuid": session.uuid}))

        self.assertEquals(response.status_code, 200)
