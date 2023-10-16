from sleepwalker.apps.logs_sessions.serializers.logs_session_serializer import LogsSessionSerializer
from sleepwalker.apps.logs_sessions.serializers.environment_sensors_logs_serializer import EnvironmentSensorsLogsSerializer
from sleepwalker.apps.logs_sessions.serializers.body_sensors_logs_serializer import BodySensorsLogsSerializer


logs_sessions = {
    "parameters": [],
    "description": "Get logs sessions",
    "operation_id": "get_logs_sessions",
    "tags": ["logs_sessions"],
    "request": None,
    "responses": {
        200: LogsSessionSerializer(many=True),
        401: None
    }
}


create_logs_session = {
    "parameters": [],
    "description": "Create logs sessions",
    "operation_id": "create_logs_session",
    "tags": ["logs_sessions"],
    "request": None,
    "responses": {
        200: None,
        201: LogsSessionSerializer
    }
}

logs_session = {
    "description": "get logs session by id",
    "operation_id": "get_logs_session",
    "tags": ["logs_sessions"],
    "request": None,
    "responses": {
        200: LogsSessionSerializer,
        401: None,
        404: None
    }
}


close_logs_session = {
    "description": "close logs session by id",
    "operation_id": "close_logs_session",
    "tags": ["logs_sessions"],
    "request": None,
    "responses": {
        200: None,
        401: None,
        404: None
    }
}


delete_logs_session = {
    "description": "delete logs session by id",
    "operation_id": "delete_logs_session",
    "tags": ["logs_sessions"],
    "request": None,
    "responses": {
        200: None,
        401: None,
        404: None
    }
}


body_sensors_logs = {
    "description": "get body sensor logs for session",
    "operation_id": "body_sensors_logs",
    "tags": ["body_sensors_logs"],
    "request": None,
    "responses": {
        200: BodySensorsLogsSerializer(many=True),
        401: None,
        404: None
    }
}


create_body_sensors_log = {
    "description": "create body sensor logs for session",
    "operation_id": "create_body_sensors_log",
    "tags": ["body_sensors_logs"],
    "request": BodySensorsLogsSerializer,
    "responses": {
        200: BodySensorsLogsSerializer,
        401: None,
        404: None
    }
}


environment_sensors_logs = {
    "description": "get environment sensor logs for session",
    "operation_id": "environment_sensors_logs",
    "tags": ["environment_sensors_logs"],
    "request": None,
    "responses": {
        200: EnvironmentSensorsLogsSerializer(many=True),
        401: None,
        404: None
    }
}


create_environment_sensors_log = {
    "description": "create environment sensor logs for session",
    "operation_id": "create_environment_sensors_log",
    "tags": ["environment_sensors_logs"],
    "request": EnvironmentSensorsLogsSerializer,
    "responses": {
        200: EnvironmentSensorsLogsSerializer,
        401: None,
        404: None
    }
}
