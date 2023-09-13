from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.serializers.environment_sensors_logs_serializer import EnvironmentSensorsLogsSerializer


@api_view(["GET"])
@authentication_classes([TokenAuth])
def environment_sensors_logs(request, session_uuid):
    log_session = get_object_or_404(models.LogsSession, uuid=session_uuid)
    serializer = EnvironmentSensorsLogsSerializer(log_session.environment_sensors_logs, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([ApiKeyAuth])
def create_environment_sensors_log(request, session_uuid):
    serializer = EnvironmentSensorsLogsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(session_uuid=session_uuid)

        return Response(status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
