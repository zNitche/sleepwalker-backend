from rest_framework import serializers
from sleepwalker.apps.logs_sessions import models


class EnvironmentSensorsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EnvironmentSensorsLog
        fields = ["date", "temperature", "humidity"]
        read_only_fields = ["date"]

    def create(self, validated_data):
        log_session = models.LogsSession.objects.filter(uuid=validated_data["session_uuid"]).first()
        obj = models.EnvironmentSensorsLog(
            temperature=validated_data["temperature"],
            humidity=validated_data["humidity"],
            log_session=log_session
        )

        obj.save()

        return obj
