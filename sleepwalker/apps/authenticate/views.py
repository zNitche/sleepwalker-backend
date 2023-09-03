from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from django.contrib.auth import authenticate
from sleepwalker.apps.authenticate import serializers
from sleepwalker.apps.authenticate import models
from sleepwalker.apps.authenticate.token_auth import TokenAuth


@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = authenticate(username=username, password=password)

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
