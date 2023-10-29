from rest_framework.test import APITestCase, override_settings
from django.contrib.auth import get_user_model
from sleepwalker.apps.authenticate import models
import datetime


@override_settings(TESTING=True)
class TestModels(APITestCase):
    def setUp(self):
        self.username = "user"
        self.password = "1234"

        get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_new_user_creation(self):
        get_user_model().objects.create_user(username="test_user", password="1234")
        user = get_user_model().objects.filter(username="test_user").first()

        self.assertIsNot(user, None)
        self.assertIsNot(user.settings, None)

    def test_existing_user(self):
        user = get_user_model().objects.filter(username=self.username).first()

        self.assertIsNot(user, None)

    def test_auth_token_creation(self):
        user = get_user_model().objects.filter(username=self.username).first()
        token = models.AuthToken.objects.create(user=user)

        self.assertIsNot(token, None)
        self.assertTrue(token.is_valid())
        self.assertFalse(token.is_expired())

    def test_auth_token_blacklist(self):
        user = get_user_model().objects.filter(username=self.username).first()
        token = models.AuthToken.objects.create(user=user, blacklisted=True)

        self.assertFalse(token.is_valid())

    def test_auth_token_expiration(self):
        user = get_user_model().objects.filter(username=self.username).first()
        past_date = datetime.datetime.utcnow() - datetime.timedelta(1)
        token = models.AuthToken.objects.create(user=user, expiration_date=past_date)

        self.assertFalse(token.is_valid())
        self.assertTrue(token.is_expired())
