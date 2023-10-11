from sleepwalker.apps.authenticate import models
from rest_framework import authentication
from rest_framework import exceptions


class ApiKeyAuth(authentication.BaseAuthentication):
    def authenticate_header(self, request):
        return "Token"

    def authenticate(self, request):
        token = request.META.get("HTTP_X_AUTHORIZATION")
        api_key = request.META.get("HTTP_X_API_KEY")

        if token is None:
            if api_key:
                user = models.User.objects.filter(api_key=api_key).first()
                if user:
                    return (user, None)

            raise exceptions.AuthenticationFailed("Invalid or missing api key")
