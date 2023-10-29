from django.contrib import admin
from sleepwalker.apps.authenticate import models
from sleepwalker.apps.authenticate import admin_models


# Register your models here.
admin.site.register(models.User, admin_models.CustomUserAdmin)
admin.site.register(models.AuthToken, admin_models.AuthTokenAdmin)
admin.site.register(models.Settings, admin_models.SettingsAdmin)
