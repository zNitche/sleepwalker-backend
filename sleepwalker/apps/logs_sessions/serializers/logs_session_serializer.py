from rest_framework import serializers
from sleepwalker.apps.logs_sessions import models


class LogsSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogsSession
        fields = ["uuid", "start_date", "end_date"]
        read_only_fields = ["uuid", "start_date", "end_date"]
