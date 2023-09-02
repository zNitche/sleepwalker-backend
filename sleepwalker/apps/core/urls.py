from django.urls import path
from sleepwalker.apps.core import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
]
