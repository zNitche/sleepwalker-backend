from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import authenticate_schema as docs_schema
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.authenticate import serializers
from sleepwalker.utils import tokens_utils


class ApiKeyView(APIView):
    authentication_classes = [TokenAuth]

    @extend_schema(**docs_schema.get_api_key)
    def get(self, request, *args, **kwargs):
        current_user = request.auth.user
        serializer = serializers.UserApiKeySerializer(current_user)

        return Response(serializer.data)

    @extend_schema(**docs_schema.create_api_key)
    def post(self, request, *args, **kwargs):
        current_user = request.auth.user
        current_user.api_key = tokens_utils.generate_api_key()
        current_user.save()

        serializer = serializers.UserApiKeySerializer(current_user)

        return Response(serializer.data)
