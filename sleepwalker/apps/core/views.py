from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from sleepwalker.apps.core import serializers
from sleepwalker.apps.core import models
from sleepwalker.apps.authenticate.token_auth import TokenAuth


@api_view(["GET"])
@authentication_classes([TokenAuth])
def log_sessions(request):
    log_sessions_for_user = models.LogSession.objects.filter(user=request.user).all()
    serializer = serializers.LogSessionSerializer(log_sessions_for_user, many=True)

    return Response(serializer.data)
