from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sleepwalker.apps.core import models
from sleepwalker.apps.core.paginators import LogSessionsPagination
from sleepwalker.apps.authenticate.token_auth import TokenAuth
from sleepwalker.apps.core.serializers.log_session_serializer import LogSessionSerializer


class LogSessionsView(APIView):
    authentication_classes = [TokenAuth]

    def get(self, request, *args, **kwargs):
        log_sessions_for_user = models.LogSession.objects.filter(user=request.user).order_by("-start_date").all()

        paginator = LogSessionsPagination()
        page_results = paginator.paginate_queryset(log_sessions_for_user, request)
        serializer = LogSessionSerializer(page_results, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        model = models.LogSession()
        model.save()

        return Response(status=status.HTTP_201_CREATED)
