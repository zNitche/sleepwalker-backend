from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.paginators import LogsSessionsPagination
from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer
from sleepwalker.utils import models_utils


@api_view(["GET"])
@authentication_classes([TokenAuth])
def logs_sessions(request):
    log_sessions_for_user = models.LogsSession.objects.filter(user=request.user).order_by("-start_date").all()

    paginator = LogsSessionsPagination()
    page_results = paginator.paginate_queryset(log_sessions_for_user, request)
    serializer = LogsSessionSerializer(page_results, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@authentication_classes([ApiKeyAuth])
def create_logs_session(request):
    if not models_utils.check_if_user_has_unfinished_session(request.user.id):
        session = models.LogsSession.objects.create(user=request.user)
        serializer = LogsSessionSerializer(session)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_200_OK)
