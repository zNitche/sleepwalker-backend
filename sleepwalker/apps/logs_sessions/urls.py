from django.urls import path
from sleepwalker.apps.logs_sessions.views import logs_sessions_views, logs_session_views
from sleepwalker.apps.logs_sessions.class_views.body_sensors_logs_view import BodySenorsLogsView
from sleepwalker.apps.logs_sessions.class_views.environment_sensors_logs_view import EnvironmentSensorsLogsView

app_name = "sessions"

urlpatterns = [
    path("", logs_sessions_views.logs_sessions, name="logs_sessions"),
    path("init/", logs_sessions_views.create_logs_session, name="create_logs_session"),
    path("<str:session_uuid>/", logs_session_views.logs_session, name="logs_session"),
    path("<str:session_uuid>/close/", logs_session_views.close_logs_session, name="close_logs_session"),
    path("<str:session_uuid>/remove/", logs_session_views.remove_logs_session, name="remove_logs_session"),

    # path("<str:session_uuid>/body-sensors/add", BodySenorsLogsView.as_view(), name="add_body_sensors_log"),
    # path("<str:session_uuid>/environment-sensors/add", EnvironmentSensorsLogsView.as_view(), name="add_environment_sensors_log"),
    #
    # path("<str:session_uuid>/body-sensors/", BodySenorsLogsView.as_view(), name="body_sensors_logs"),
    # path("<str:session_uuid>/environment-sensors/", EnvironmentSensorsLogsView.as_view(), name="environment_sensors_logs"),
]
