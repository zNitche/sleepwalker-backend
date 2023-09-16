from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from sleepwalker.apps.logs_sessions import models
from datetime import datetime


class TestModels(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_create_logs_session(self):
        session = models.LogsSession.objects.create(user=self.user)

        self.assertEquals(session.user, self.user)
        self.assertIsNot(session, None)
        self.assertIsNot(session.start_date, None)
        self.assertIs(session.end_date, None)

        session.end_date = datetime.utcnow()
        session.save()

        self.assertIsNot(session.end_date, None)

    def test_create_body_sensors_log(self):
        session = models.LogsSession.objects.create(user=self.user)
        log = models.BodySensorsLog.objects.create(log_session=session,
                                                   heart_beat=5,
                                                   acceleration_x=1,
                                                   acceleration_y=2,
                                                   acceleration_z=3)

        self.assertIsNot(session, None)
        self.assertIs(log.log_session, session)
        self.assertTrue(log in session.body_sensors_logs.all())

    def test_create_env_sensors_log(self):
        session = models.LogsSession.objects.create(user=self.user)
        log = models.EnvironmentSensorsLog.objects.create(log_session=session,
                                                          temperature=5,
                                                          humidity=1)

        self.assertIsNot(session, None)
        self.assertIs(log.log_session, session)
        self.assertTrue(log in session.environment_sensors_logs.all())
