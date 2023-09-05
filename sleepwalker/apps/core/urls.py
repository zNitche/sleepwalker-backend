from django.urls import path
from sleepwalker.apps.core import views
from sleepwalker.apps.core.class_views.body_sensors_view import BodySenorsView

app_name = "core"

urlpatterns = [
    path("", views.log_sessions, name="log_sessions"),
    path("<str:session_uuid>/body-sensors/", BodySenorsView.as_view(), name="body_sensors"),
    path("<str:session_uuid>/environment-sensors/", views.environment_sensors, name="environment_sensors"),
]
