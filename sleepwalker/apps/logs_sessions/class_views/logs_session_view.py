from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from datetime import datetime


class LogsSessionView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogsSession, uuid=self.kwargs["session_uuid"])
        serializer = LogsSessionSerializer(log_session)

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogsSession, uuid=self.kwargs["session_uuid"])
        log_session.end_date = datetime.utcnow()
        log_session.save()

        return Response(status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogsSession, uuid=self.kwargs["session_uuid"])
        log_session.delete()

        return Response(status=status.HTTP_200_OK)
