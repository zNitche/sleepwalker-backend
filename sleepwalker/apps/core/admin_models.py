from django.contrib.admin import ModelAdmin


class LogSessionAdmin(ModelAdmin):
    list_display = ("uuid", "start_date", "end_date", "user_id")
    search_fields = ("user_id", "uuid")

    readonly_fields = ["uuid"]


class BodySensorsLogAdmin(ModelAdmin):
    list_display = ("uuid", "hear_beat", "acceleration_x", "acceleration_y", "acceleration_z", "date", "log_session")
    search_fields = ("log_session", "uuid")

    readonly_fields = ["uuid"]


class EnvironmentSensorsLogAdmin(ModelAdmin):
    list_display = ("uuid", "temperature", "humidity", "log_session")
    search_fields = ("log_session", "uuid")

    readonly_fields = ["uuid"]
