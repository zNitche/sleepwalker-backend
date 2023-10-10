from sleepwalker.celery_tasks.task_base import TaskBase
from sleepwalker.apps.authenticate import models
from sleepwalker.consts import TasksDelays
import time


class SleepwalkingDetectionProcess(TaskBase):
    def __init__(self):
        super().__init__()

        self.users = models.User.objects.all()

    def mainloop(self):
        try:
            while self.is_running:
                time.sleep(TasksDelays.SLEEPWALKING_DETECTION_DELAY)

        except Exception as e:
            self.logger.error(f"[{self.get_process_name()}] - {str(e)}")
