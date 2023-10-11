from sleepwalker.apps.authenticate import models
from rest_framework import authentication
from rest_framework import exceptions


class TokenAuth(authentication.BaseAuthentication):
    def authenticate_header(self, request):
        return "Token"

    def authenticate(self, request):
        token = request.META.get("HTTP_X_AUTHORIZATION")

        if token:
            auth_token = models.AuthToken.objects.filter(key=token).first()
            if auth_token and auth_token.is_valid():
                user = auth_token.user

                if user:
                    return (user, auth_token)

        raise exceptions.AuthenticationFailed("Invalid or missing auth token")
