from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from sleepwalker.apps.authenticate.models import AuthToken
from sleepwalker.apps.logs_sessions import models
from sleepwalker.utils import tokens_utils


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
        response = self.client.get("/api/sessions/")
        self.assertEquals(response.status_code, 401)

    def test_logs_sessions(self):
        self.client.credentials(HTTP_X_AUTHORIZATION=self.auth_token.key)
        response = self.client.get(f"/api/sessions/")

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json().get("data")), 0)

    def test_init_logs_session_not_auth(self):
        response = self.client.post("/api/sessions/init/")
        self.assertEquals(response.status_code, 401)

    def test_init_logs_session(self):
        self.client.credentials(HTTP_X_API_KEY=self.user.api_key)
        response = self.client.post(f"/api/sessions/init/")
        session_uuid = response.json().get("uuid")

        self.assertEquals(response.status_code, 201)
        self.assertIsNot(session_uuid, None)

        session = models.LogsSession.objects.filter(uuid=session_uuid).first()
        self.assertIsNot(session, None)
