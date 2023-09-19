from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth


@api_view(["GET"])
def health_check(request):
    return Response(status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def auth_check(request):
    return Response(status.HTTP_200_OK)
