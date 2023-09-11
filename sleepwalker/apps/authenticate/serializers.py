from rest_framework import serializers
from sleepwalker.apps.authenticate import models


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthToken
        fields = ["token"]


class UserApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["api_key"]
