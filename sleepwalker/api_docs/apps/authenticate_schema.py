from sleepwalker.apps.authenticate import serializers


login = {
    "parameters": [],
    "description": "Login",
    "operation_id": "auth_login",
    "tags": ["auth"],
    "request": serializers.LoginSerializer,
    "responses": {
        200:  serializers.AuthTokenSerializer
    }
}


logout = {
    "parameters": [],
    "description": "Logout",
    "operation_id": "auth_logout",
    "tags": ["auth"],
    "request": None,
    "responses": {
        200:  None,
        401:  None
    }
}


create_api_key = {
    "parameters": [],
    "description": "Create API Key",
    "operation_id": "auth_create_api_key",
    "request": None,
    "responses": {
        200:  serializers.UserApiKeySerializer,
        401:  None
    }
}


get_api_key = {
    "parameters": [],
    "description": "Get API Key",
    "operation_id": "auth_get_api_key",
    "request": None,
    "responses": {
        200:  serializers.UserApiKeySerializer,
        401:  None
    }
}
