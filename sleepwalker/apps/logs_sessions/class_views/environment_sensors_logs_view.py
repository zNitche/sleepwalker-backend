from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.serializers.environment_sensors_logs_serializer import EnvironmentSensorsLogsSerializer
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth


class EnvironmentSensorsLogsView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogsSession, uuid=self.kwargs["session_uuid"])
        serializer = EnvironmentSensorsLogsSerializer(log_session.environment_sensors_logs, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        session_uuid = self.kwargs["session_uuid"]
        serializer = EnvironmentSensorsLogsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session_uuid=session_uuid)

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
