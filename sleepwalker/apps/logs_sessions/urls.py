from django.urls import path
from sleepwalker.apps.logs_sessions.views import (logs_sessions_views, logs_session_views,
                                                  body_sensors_logs_views, environment_sensors_logs_views)

app_name = "sessions"

urlpatterns = [
    path("", logs_sessions_views.logs_sessions, name="logs_sessions"),
    path("init/", logs_sessions_views.create_logs_session, name="create_logs_session"),
    path("<str:session_uuid>/", logs_session_views.logs_session, name="logs_session"),
    path("<str:session_uuid>/close/", logs_session_views.close_logs_session, name="close_logs_session"),
    path("<str:session_uuid>/remove/", logs_session_views.remove_logs_session, name="remove_logs_session"),

    path("<str:session_uuid>/body-sensors/add", body_sensors_logs_views.create_body_sensors_log,
         name="create_body_sensors_log"),
    path("<str:session_uuid>/environment-sensors/add", environment_sensors_logs_views.create_environment_sensors_log,
         name="create_environment_sensors_log"),

    path("<str:session_uuid>/body-sensors/", body_sensors_logs_views.body_sensors_logs,
         name="body_sensors_logs"),
    path("<str:session_uuid>/environment-sensors/", environment_sensors_logs_views.environment_sensors_logs,
         name="environment_sensors_logs"),
]
