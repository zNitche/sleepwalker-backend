from rest_framework import serializers
from sleepwalker.apps.logs_sessions import models


class SleepwalkingEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SleepwalkingEvent
        fields = ["start_date", "end_date"]
        read_only_fields = ["start_date", "end_date"]
