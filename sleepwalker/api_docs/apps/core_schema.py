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


reset_logs_session = {
    "description": "reset current logs session",
    "operation_id": "reset_logs_session",
    "tags": ["core"],
    "request": None,
    "responses": {
        200: None,
        401: None,
        404: None
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
