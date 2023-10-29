from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import authenticate_schema as docs_schema
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.authenticate import serializers


class SettingsView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(**docs_schema.get_user_settings)
    def get(self, request, *args, **kwargs):
        current_user = request.auth.user
        serializer = serializers.UserSettingsSerializer(current_user.settings)

        return Response(serializer.data)

    @extend_schema(**docs_schema.update_user_settings)
    def put(self, request, *args, **kwargs):
        current_user = request.auth.user
        serializer = serializers.UserSettingsSerializer(current_user.settings, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
