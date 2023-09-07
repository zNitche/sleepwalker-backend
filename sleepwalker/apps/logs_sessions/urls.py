from django.urls import path
from sleepwalker.apps.logs_sessions.class_views.body_sensors_logs_view import BodySenorsLogsView
from sleepwalker.apps.logs_sessions.class_views.environment_sensors_logs_view import EnvironmentSensorsLogsView
from sleepwalker.apps.logs_sessions.class_views.logs_session_view import LogsSessionView
from sleepwalker.apps.logs_sessions.class_views.logs_sessions_view import LogsSessionsView

app_name = "sessions"

urlpatterns = [
    path("", LogsSessionsView.as_view(),
         name="logs_sessions"),
    path("<str:session_uuid>/", LogsSessionView.as_view(),
         name="logs_session"),
    path("<str:session_uuid>/body-sensors/", BodySenorsLogsView.as_view(),
         name="body_sensors_logs"),
    path("<str:session_uuid>/environment-sensors/", EnvironmentSensorsLogsView.as_view(),
         name="environment_sensors_logs"),
]
