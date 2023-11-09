from sleepwalker.apps.core import serializers


health_check = {
    "parameters": [],
    "description": "Health check",
    "operation_id": "health_check",
    "tags": ["core"],
    "request": None,
    "responses": {
        200: None
    }
}


auth_check = {
    "parameters": [],
    "description": "Auth check",
    "operation_id": "auth_check",
    "tags": ["core"],
    "request": None,
    "responses": {
        200: None,
        401: None
    }
}


event_detected = {
    "parameters": [],
    "description": "Sleepwalking event detected",
    "operation_id": "event_detected",
    "tags": ["core"],
    "request": None,
    "responses": {
        200: None,
        404: None,
        401: None
    }
}


get_user_settings = {
    "parameters": [],
    "description": "Get user settings",
    "tags": ["user"],
    "request": None,
    "responses": {
        200:  serializers.UserSettingsSerializer,
        401:  None
    }
}


update_user_settings = {
    "parameters": [],
    "description": "Update user settings",
    "tags": ["user"],
    "request": serializers.UserSettingsSerializer,
    "responses": {
        200:  serializers.UserSettingsSerializer,
        400: serializers.UserSettingsSerializer.errors,
        401:  None
    }
}
