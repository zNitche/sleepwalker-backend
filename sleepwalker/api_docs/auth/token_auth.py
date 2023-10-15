from drf_spectacular.openapi import OpenApiAuthenticationExtension
from sleepwalker.apps.authenticate.auth_handlers.token_auth import TokenAuth


class TokenAuthSchema(OpenApiAuthenticationExtension):
    target_class = TokenAuth
    name = "TokenAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Auth Token obtained from login process"
        }
