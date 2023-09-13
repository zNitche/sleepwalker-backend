from django.urls import path
from sleepwalker.apps.core import views

app_name = "core"

urlpatterns = [
    path("health-check/", views.health_check, name="health_check"),
    path("auth-check/", views.auth_check, name="auth_check"),
]
