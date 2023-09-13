from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from django.shortcuts import get_object_or_404
from rest_framework import status
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer
from datetime import datetime


@api_view(["GET"])
@authentication_classes([TokenAuth])
def logs_session(request, session_uuid):
    log_session = get_object_or_404(models.LogsSession, uuid=session_uuid)
    serializer = LogsSessionSerializer(log_session)

    return Response(serializer.data)


@api_view(["PUT"])
@authentication_classes([ApiKeyAuth])
def close_logs_session(request, session_uuid):
    log_session = get_object_or_404(models.LogsSession, uuid=session_uuid)
    log_session.end_date = datetime.utcnow()
    log_session.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@authentication_classes([TokenAuth])
def remove_logs_session(request, session_uuid):
    log_session = get_object_or_404(models.LogsSession, uuid=session_uuid)
    log_session.delete()

    return Response(status=status.HTTP_200_OK)
