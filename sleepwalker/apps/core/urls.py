from django.urls import path
from sleepwalker.apps.core import views
from sleepwalker.apps.core.class_views.body_sensors_view import BodySenorsView
from sleepwalker.apps.core.class_views.environment_sensors_view import EnvironmentSensorsView
from sleepwalker.apps.core.class_views.log_session_view import LogSessionView
from sleepwalker.apps.core.class_views.log_sessions_view import LogSessionsView

app_name = "core"

urlpatterns = [
    path("", views.healthcheck,
         name="healthcheck"),
    path("sessions/", LogSessionsView.as_view(),
         name="log_sessions"),
    path("sessions/<str:session_uuid>/", LogSessionView.as_view(),
         name="log_session"),
    path("sessions/<str:session_uuid>/body-sensors/", BodySenorsView.as_view(),
         name="body_sensors"),
    path("sessions/<str:session_uuid>/environment-sensors/", EnvironmentSensorsView.as_view(),
         name="environment_sensors"),
]
