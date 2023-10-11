from sleepwalker.apps.authenticate import models
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth
from rest_framework import exceptions


class ApiKeyAuthStandalone(ApiKeyAuth):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")

        if api_key:
            user = models.User.objects.filter(api_key=api_key).first()
            if user:
                return (user, None)

        raise exceptions.AuthenticationFailed("Invalid or missing api key")
