from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.authenticate.token_auth import TokenAuth
from sleepwalker.apps.logs_sessions.paginators import LogsSessionsPagination
from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer


class LogsSessionsView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_sessions_for_user = models.LogsSession.objects.filter(user=request.user).order_by("-start_date").all()

        paginator = LogsSessionsPagination()
        page_results = paginator.paginate_queryset(log_sessions_for_user, request)
        serializer = LogsSessionSerializer(page_results, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        model = models.LogsSession(user=request.user)
        model.save()

        return Response(status=status.HTTP_201_CREATED)
