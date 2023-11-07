from django.urls import path
from sleepwalker.apps.core import views
from sleepwalker.apps.core.class_views.settings_view import SettingsView

app_name = "core"

urlpatterns = [
    path("health-check/", views.health_check, name="health_check"),
    path("auth-check/", views.auth_check, name="auth_check"),
    path("event-detected/", views.event_detected, name="event_detected"),
    path("reset-current-session/", views.reset_logs_session, name="reset_logs_session"),

    path("user/settings/", SettingsView.as_view(), name="user_settings")
]
