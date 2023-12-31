from django.db import models
from django.contrib.auth import get_user_model
from sleepwalker.utils import tokens_utils
import datetime


class LogsSession(models.Model):
    uuid = models.CharField(max_length=32, unique=True, null=False, default=tokens_utils.generate_uuid)

    start_date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)
    end_date = models.DateTimeField(null=True, default=None)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False,
                             related_name="log_sessions")

    def __str__(self):
        return self.uuid


class BodySensorsLog(models.Model):
    heart_beat = models.FloatField(null=False, default=0)
    acceleration_x = models.FloatField(null=False, default=0)
    acceleration_y = models.FloatField(null=False, default=0)
    acceleration_z = models.FloatField(null=False, default=0)

    date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)

    log_session = models.ForeignKey(LogsSession, on_delete=models.CASCADE, null=False,
                                    related_name="body_sensors_logs")


class EnvironmentSensorsLog(models.Model):
    temperature = models.FloatField(null=False, default=0)
    humidity = models.FloatField(null=False, default=0)

    date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)

    log_session = models.ForeignKey(LogsSession, on_delete=models.CASCADE, null=False,
                                    related_name="environment_sensors_logs")


class SleepwalkingEvent(models.Model):
    start_date = models.DateTimeField(null=False, default=datetime.datetime.utcnow)
    end_date = models.DateTimeField(null=True, default=None)

    logs_session = models.ForeignKey(LogsSession, on_delete=models.CASCADE, null=False,
                                     related_name="sleepwalking_events")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False,
                             related_name="sleepwalking_events")
