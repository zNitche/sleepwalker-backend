from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import status
from drf_spectacular.utils import extend_schema
from sleepwalker.api_docs.apps import logs_sessions_schema as docs_schema
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions.paginators import LogsSessionsPagination
from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer
from sleepwalker.apps.logs_sessions.serializers.statistics_serializer import StatisticsSerializer
from sleepwalker.utils import models_utils, tasks_utils
from sleepwalker.apps.core import tasks as celery_tasks
from sleepwalker.utils.filtersUtils import get_logs_sessions_filters


@extend_schema(**docs_schema.logs_sessions)
@api_view(["GET"])
@authentication_classes([TokenAuth])
def logs_sessions(request):
    filters = get_logs_sessions_filters(request.GET)
    log_sessions_for_user = models.LogsSession.objects.filter(user=request.user, **filters).order_by("-start_date").all()

    paginator = LogsSessionsPagination()
    page_results = paginator.paginate_queryset(log_sessions_for_user, request)
    serializer = LogsSessionSerializer(page_results, many=True)

    return paginator.get_paginated_response(serializer.data)


@extend_schema(**docs_schema.latest_running_logs_session)
@api_view(["GET"])
@authentication_classes([TokenAuth])
def latest_running_logs_session(request):
    latest_session = models.LogsSession.objects.filter(user=request.user).order_by("-start_date").first()

    if latest_session and latest_session.end_date is None:
        return Response(LogsSessionSerializer(latest_session).data, status=status.HTTP_200_OK)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@extend_schema(**docs_schema.reset_current_logs_session)
@api_view(["POST"])
@authentication_classes([ApiKeyAuth, TokenAuth])
def reset_current_logs_session(request):
    detected_for_user = tasks_utils.check_if_sleepwalking_detected_for_user(request.user.id)

    if detected_for_user:
        tasks_utils.reset_sleepwalking_logger_for_user(request.user.id)

    response_status = status.HTTP_200_OK if detected_for_user else status.HTTP_204_NO_CONTENT
    return Response(response_status)


@extend_schema(**docs_schema.create_logs_session)
@api_view(["POST"])
@authentication_classes([ApiKeyAuth])
def create_logs_session(request):
    if not models_utils.check_if_user_has_unfinished_session(request.user.id):
        session = models.LogsSession.objects.create(user=request.user)
        serializer = LogsSessionSerializer(session)

        user = request.user
        settings = {
            "sw_detection_heart_beat_percentage_threshold": user.settings.sw_detection_heart_beat_percentage_threshold
        }

        tasks_utils.run_task(celery_tasks.SleepwalkingDetectionProcess, (user.id, settings, session.uuid))

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    else:
        return Response(status=status.HTTP_200_OK)


@extend_schema(**docs_schema.logs_sessions_statistics)
@api_view(["GET"])
@authentication_classes([TokenAuth])
def logs_sessions_statistics(request):
    log_sessions_for_user = models.LogsSession.objects.filter(user=request.user).order_by("-start_date")

    first_session = log_sessions_for_user.last()
    last_session = log_sessions_for_user.first()

    data = {
        "logs_sessions": log_sessions_for_user.count(),
        "first_session_start_date": first_session.start_date if first_session else None,
        "last_session_start_date": last_session.start_date if last_session else None,
        "first_session_end_date": first_session.end_date if first_session else None,
        "last_session_end_date": last_session.end_date if last_session else None,
        "sleepwalking_events_count": request.user.sleepwalking_events.count(),
        "sleepwalking_events": models_utils.get_latest_sleepwalking_events_count(request.user.id)
    }

    serializer = StatisticsSerializer(data)

    return Response(serializer.data, status=status.HTTP_200_OK)
