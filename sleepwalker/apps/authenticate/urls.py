from django.urls import path
from sleepwalker.apps.authenticate import views
from sleepwalker.apps.authenticate.class_views.api_key_view import ApiKeyView

app_name = "authenticate"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api-key/", ApiKeyView.as_view(), name="api_key"),
]
