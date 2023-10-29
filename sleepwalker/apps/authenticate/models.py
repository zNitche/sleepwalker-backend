from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth import get_user_model
import datetime
from sleepwalker.apps.authenticate.managers import UserManager
from sleepwalker.utils import tokens_utils


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=25, unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=datetime.datetime.utcnow)

    api_key = models.CharField(max_length=16, unique=True, null=True, default=None)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    sw_detection_heart_beat_percentage_threshold = models.IntegerField(null=False, default=25)

    def __str__(self):
        return self.user.username


class AuthToken(models.Model):
    key = models.CharField(max_length=256, unique=True, null=False, default=tokens_utils.generate_token)
    creation_date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)
    expiration_date = models.DateTimeField(null=False, default=tokens_utils.get_token_expiration_date)
    blacklisted = models.BooleanField(null=False, default=False)

    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="auth_tokens")

    def __str__(self):
        return self.short_key()

    def is_expired(self):
        return True if datetime.datetime.utcnow() > self.expiration_date else False

    def is_valid(self):
        return False if self.is_expired() or self.blacklisted else True

    def short_key(self):
        return self.key[:10]
