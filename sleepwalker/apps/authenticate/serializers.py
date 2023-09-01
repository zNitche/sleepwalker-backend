from rest_framework import serializers
from sleepwalker.apps.authenticate.models import AuthToken


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthToken
        fields = ["token"]
