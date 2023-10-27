from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import core_schema as docs_schema
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.utils import tasks_utils


@extend_schema(**docs_schema.health_check)
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def health_check(request):
    return Response(status=status.HTTP_200_OK)


@extend_schema(**docs_schema.auth_check)
@api_view(["GET"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def auth_check(request):
    return Response(status=status.HTTP_200_OK)


@extend_schema(**docs_schema.event_detected)
@api_view(["GET"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def event_detected(request):
    detected_for_user = tasks_utils.check_if_sleepwalking_detected_for_user(request.user.id)

    response_status = status.HTTP_200_OK if detected_for_user else status.HTTP_204_NO_CONTENT
    return Response(status=response_status)


@extend_schema(**docs_schema.reset_logs_session)
@api_view(["POST"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def reset_logs_session(request):
    detected_for_user = tasks_utils.check_if_sleepwalking_detected_for_user(request.user.id)

    if detected_for_user:
        tasks_utils.reset_sleepwalking_logger_for_user(request.user.id)

    response_status = status.HTTP_200_OK if detected_for_user else status.HTTP_204_NO_CONTENT
    return Response(response_status)
