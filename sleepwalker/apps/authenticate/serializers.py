from rest_framework import serializers
from sleepwalker.apps.authenticate import models


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ["username", "password"]


class AuthTokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source="key")

    class Meta:
        model = models.AuthToken
        fields = ["token"]


class UserApiKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["api_key"]


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = ["sw_detection_heart_beat_percentage_threshold"]
