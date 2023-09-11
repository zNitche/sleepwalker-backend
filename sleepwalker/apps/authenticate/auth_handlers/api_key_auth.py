from sleepwalker.apps.authenticate import models
from rest_framework import authentication
from rest_framework import exceptions


class ApiKeyAuth(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.META.get("HTTP_X_API_KEY")

        try:
            user = models.User.objects.filter(api_key=api_key).first()

            if user:
                return (user, None)

        except Exception as e:
            pass

        raise exceptions.AuthenticationFailed("Invalid or missing api key")
