from django.urls import path
from sleepwalker.apps.core import views

app_name = "core"

urlpatterns = [
    path("sessions/", views.log_sessions, name="log_sessions"),
    path("sessions/<str:session_uuid>/body-sensors/", views.body_sensors, name="body_sensors"),
    path("sessions/<str:session_uuid>/environment-sensors/", views.environment_sensors, name="environment_sensors"),
]
