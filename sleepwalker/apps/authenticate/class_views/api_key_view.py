from rest_framework.views import APIView
from rest_framework.response import Response
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.authenticate import serializers
from sleepwalker.utils import models_utils


class ApiKeyView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        current_user = request.auth.user
        serializer = serializers.UserApiKeySerializer(current_user)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        current_user = request.auth.user
        current_user.api_key = models_utils.generate_api_key()
        current_user.save()

        serializer = serializers.UserApiKeySerializer(current_user)

        return Response(serializer.data)
