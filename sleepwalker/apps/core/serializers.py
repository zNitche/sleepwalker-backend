from rest_framework import serializers
from sleepwalker.apps.core import models


class LogSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogSession
        exclude = ["id", "user"]


class BodySensorsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BodySensorsLog
        exclude = ["id", "log_session"]


class EnvironmentSensorsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnvironmentSensorsLog
        exclude = ["id", "log_session"]
