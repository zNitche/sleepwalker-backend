from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import core_schema as docs_schema
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth


@extend_schema(**docs_schema.health_check)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return Response(status.HTTP_200_OK)


@extend_schema(**docs_schema.auth_check)
@api_view(["GET"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def auth_check(request):
    return Response(status.HTTP_200_OK)


@extend_schema(**docs_schema.event_detected)
@api_view(["GET"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def event_detected(request):
    return Response(status.HTTP_200_OK)
