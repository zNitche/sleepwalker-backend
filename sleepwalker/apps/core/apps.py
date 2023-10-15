from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sleepwalker.apps.core'
    label = 'core'

    def ready(self):
        from sleepwalker import api_schema
