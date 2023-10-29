from django.urls import path
from sleepwalker.apps.authenticate import views
from sleepwalker.apps.authenticate.class_views.api_key_view import ApiKeyView
from sleepwalker.apps.authenticate.class_views.settings_view import SettingsView

app_name = "authenticate"

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("api-key/", ApiKeyView.as_view(), name="api_key"),
    path("user/settings/", SettingsView.as_view(), name="user_settings")
]
