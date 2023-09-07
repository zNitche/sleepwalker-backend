from django.urls import path
from sleepwalker.apps.core import views
from sleepwalker.apps.core.class_views.body_sensors_logs_view import BodySenorsLogsView
from sleepwalker.apps.core.class_views.environment_sensors_logs_view import EnvironmentSensorsLogsView
from sleepwalker.apps.core.class_views.logs_session_view import LogsSessionView
from sleepwalker.apps.core.class_views.logs_sessions_view import LogsSessionsView

app_name = "core"

urlpatterns = [
    path("", views.healthcheck,
         name="healthcheck"),
    path("sessions/", LogsSessionsView.as_view(),
         name="logs_sessions"),
    path("sessions/<str:session_uuid>/", LogsSessionView.as_view(),
         name="logs_session"),
    path("sessions/<str:session_uuid>/body-sensors/", BodySenorsLogsView.as_view(),
         name="body_sensors_logs"),
    path("sessions/<str:session_uuid>/environment-sensors/", EnvironmentSensorsLogsView.as_view(),
         name="environment_sensors_logs"),
]
