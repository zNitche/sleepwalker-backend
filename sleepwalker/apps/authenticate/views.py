from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
from sleepwalker.apps.authenticate import serializers
from sleepwalker.apps.authenticate import models


@api_view(["POST"])
def login(request):
    username = request.data["username"]
    password = request.data["password"]

    user = authenticate(username=username, password=password)

    if user:
        token = models.AuthToken(owner=user)
        token.save()

        serializer = serializers.AuthTokenSerializer(token)

        return Response(serializer.data)

    return Response(status=status.HTTP_401_UNAUTHORIZED)
