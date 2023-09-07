from rest_framework import serializers
from sleepwalker.apps.core import models


class LogSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogSession
        fields = ["uuid", "start_date", "end_date"]
        read_only_fields = ["uuid", "start_date", "end_date"]
