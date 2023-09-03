from rest_framework import serializers
from sleepwalker.apps.core import models


class LogSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogSession
        exclude = ["user"]
