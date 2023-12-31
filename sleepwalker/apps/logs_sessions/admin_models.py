from django.contrib.admin import ModelAdmin


class LogsSessionAdmin(ModelAdmin):
    list_display = ("uuid", "start_date", "end_date", "user_id")
    search_fields = ("uuid", )

    readonly_fields = ["uuid"]


class SleepwalkingEventAdmin(ModelAdmin):
    list_display = ("start_date", "end_date", "logs_session_id")

    search_fields = ("logs_session_id",)


class BodySensorsLogAdmin(ModelAdmin):
    list_display = ("heart_beat", "acceleration_x", "acceleration_y", "acceleration_z", "date", "log_session")


class EnvironmentSensorsLogAdmin(ModelAdmin):
    list_display = ("temperature", "humidity", "log_session")
