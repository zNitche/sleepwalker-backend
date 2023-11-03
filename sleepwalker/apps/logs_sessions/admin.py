from django.contrib import admin
from sleepwalker.apps.logs_sessions import models
from sleepwalker.apps.logs_sessions import admin_models

# Register your models here.
admin.site.register(models.LogsSession, admin_models.LogsSessionAdmin)
admin.site.register(models.BodySensorsLog, admin_models.BodySensorsLogAdmin)
admin.site.register(models.EnvironmentSensorsLog, admin_models.EnvironmentSensorsLogAdmin)
admin.site.register(models.SleepwalkingEvent, admin_models.SleepwalkingEventAdmin)
