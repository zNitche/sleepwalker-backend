from rest_framework import serializers
from sleepwalker.apps.core import models


class EnvironmentSensorsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnvironmentSensorsLog
        exclude = ["id", "log_session"]
