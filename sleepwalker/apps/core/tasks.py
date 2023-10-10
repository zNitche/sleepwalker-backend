from sleepwalker.celery import app
from sleepwalker.apps.core.task.sleepwalking_detection_process import SleepwalkingDetectionProcess


SleepwalkingDetectionProcess = app.register_task(SleepwalkingDetectionProcess())
