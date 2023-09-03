from django.urls import path
from sleepwalker.apps.core import views

app_name = "core"

urlpatterns = [
    path("log-sessions/", views.log_sessions, name="log_sessions"),
]
