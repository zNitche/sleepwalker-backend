from drf_spectacular.openapi import OpenApiAuthenticationExtension
from sleepwalker.apps.authenticate.auth_handlers.api_key_auth import ApiKeyAuth


class ApiKeyAuthSchema(OpenApiAuthenticationExtension):
    target_class = ApiKeyAuth
    name = "ApiKeyAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "api-key",
            "description": "api key"
        }
