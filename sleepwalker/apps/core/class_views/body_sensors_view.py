from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.core import models
from sleepwalker.apps.core.serializers.body_sensors_logs_serializer import BodySensorsLogsSerializer
from sleepwalker.apps.authenticate.token_auth import TokenAuth


class BodySenorsView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogSession, uuid=self.kwargs["session_uuid"])
        serializer = BodySensorsLogsSerializer(log_session.body_sensors_logs, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        session_uuid = self.kwargs["session_uuid"]
        serializer = BodySensorsLogsSerializer(data=request.data, context={"session_uuid": session_uuid})
        if serializer.is_valid():
            serializer.save()

            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
