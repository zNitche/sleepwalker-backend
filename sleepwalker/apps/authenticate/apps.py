from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sleepwalker.apps.authenticate'
    label = 'authenticate'

    def ready(self):
        from sleepwalker.apps.authenticate import signals
