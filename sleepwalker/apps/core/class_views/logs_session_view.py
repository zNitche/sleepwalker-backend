from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.core import models
from sleepwalker.apps.core.serializers.logs_session_serializer import LogSessionSerializer
from sleepwalker.apps.authenticate.token_auth import TokenAuth


class LogsSessionView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogSession, uuid=self.kwargs["session_uuid"])
        serializer = LogSessionSerializer(log_session)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        log_session = get_object_or_404(models.LogSession, uuid=self.kwargs["session_uuid"])
        log_session.delete()

        return Response(status=status.HTTP_200_OK)
