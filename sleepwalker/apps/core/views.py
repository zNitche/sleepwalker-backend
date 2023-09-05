from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from sleepwalker.apps.core.serializers.log_session_serializer import LogSessionSerializer
from sleepwalker.apps.core.serializers.environment_sensors_logs_serializer import EnvironmentSensorsLogsSerializer
from sleepwalker.apps.core import models
from sleepwalker.apps.authenticate.token_auth import TokenAuth
from sleepwalker.apps.core.paginators import LogSessionsPagination
from django.shortcuts import get_object_or_404


@api_view(["GET"])
@authentication_classes([TokenAuth])
def log_sessions(request):
    log_sessions_for_user = models.LogSession.objects.filter(user=request.user).order_by("-start_date").all()

    paginator = LogSessionsPagination()
    page_results = paginator.paginate_queryset(log_sessions_for_user, request)
    serializer = LogSessionSerializer(page_results, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuth])
def environment_sensors(request, session_uuid):
    log_session = get_object_or_404(models.LogSession, uuid=session_uuid)
    serializer = EnvironmentSensorsLogsSerializer(log_session.environment_sensors_logs, many=True)

    return Response(serializer.data)
