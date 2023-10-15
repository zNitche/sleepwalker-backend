from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import authenticate_schema
from sleepwalker.apps.authenticate import serializers
from sleepwalker.apps.authenticate import models
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth


@extend_schema(**authenticate_schema.login)
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = serializers.LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = authenticate(username=serializer.data.get("username"), password=serializer.data.get("password"))

        if user:
            token = models.AuthToken.objects.create(user=user)
            serializer = serializers.AuthTokenSerializer(token)

            return Response(serializer.data)

    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@authentication_classes([TokenAuth])
def logout(request):
    auth_token = request.auth
    auth_token.blacklisted = True
    auth_token.save()

    return Response(status.HTTP_200_OK)
