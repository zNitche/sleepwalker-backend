from django.contrib import admin
from sleepwalker.apps.core import models
from sleepwalker.apps.core import admin_models


# Register your models here.
admin.site.register(models.LogSession, admin_models.LogSessionAdmin)
admin.site.register(models.BodySensorsLog, admin_models.BodySensorsLogAdmin)
admin.site.register(models.EnvironmentSensorsLog, admin_models.EnvironmentSensorsLogAdmin)
