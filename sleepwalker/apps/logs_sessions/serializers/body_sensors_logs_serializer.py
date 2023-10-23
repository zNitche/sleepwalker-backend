from rest_framework import serializers
from sleepwalker.apps.logs_sessions import models


class BodySensorsLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BodySensorsLog
        fields = ["date", "heart_beat", "acceleration_x", "acceleration_y", "acceleration_z"]
        read_only_fields = ["date"]

    def create(self, validated_data):
        log_session = models.LogsSession.objects.filter(uuid=validated_data["session_uuid"]).first()
        obj = models.BodySensorsLog(
            heart_beat=validated_data["heart_beat"],
            acceleration_x=validated_data["acceleration_x"],
            acceleration_y=validated_data["acceleration_y"],
            acceleration_z=validated_data["acceleration_z"],
            log_session=log_session
        )

        obj.save()

        return obj
