from sleepwalker.apps.authenticate import models
from rest_framework import authentication
from rest_framework import exceptions


class TokenAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_X_AUTHORIZATION")

        try:
            auth_token = models.AuthToken.objects.filter(token=token).first()
            if auth_token.is_valid():
                user = auth_token.owner

                if user:
                    return (user, auth_token)

        except Exception as e:
            pass

        raise exceptions.AuthenticationFailed("Invalid or missing auth token")
