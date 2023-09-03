from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from sleepwalker.apps.core import serializers
from sleepwalker.apps.core import models
from sleepwalker.apps.authenticate.token_auth import TokenAuth
from sleepwalker.apps.core.paginators import LogSessionsPagination


@api_view(["GET"])
@authentication_classes([TokenAuth])
def log_sessions(request):
    log_sessions_for_user = models.LogSession.objects.filter(user=request.user).order_by("-start_date").all()

    paginator = LogSessionsPagination()
    page_results = paginator.paginate_queryset(log_sessions_for_user, request)
    serializer = serializers.LogSessionSerializer(page_results, many=True)

    return paginator.get_paginated_response(serializer.data)
