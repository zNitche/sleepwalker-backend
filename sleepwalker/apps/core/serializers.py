from sleepwalker.apps.authenticate.models import Settings
from rest_framework import serializers


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = ["sw_detection_heart_beat_percentage_threshold"]
