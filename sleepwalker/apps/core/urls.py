from django.urls import path
from sleepwalker.apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.healthcheck, name="healthcheck"),
]
