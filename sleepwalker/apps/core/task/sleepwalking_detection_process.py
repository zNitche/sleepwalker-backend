from sleepwalker.celery_tasks.task_base import TaskBase
from sleepwalker.consts import TasksDelays, ProcessesConsts
from sleepwalker.apps.logs_sessions import models
import time


class SleepwalkingDetectionProcess(TaskBase):
    def __init__(self):
        super().__init__()

        self.user_id = None
        self.logs_session_id = None

        self.detected = False

        self.cache_data_timeout = 60

    def run(self, user_id, logs_session_id):
        self.user_id = user_id
        self.logs_session_id = logs_session_id
        self.process_cache_key = (f"{self.user_id}_{self.logs_session_id}_"
                                  f"{self.get_process_name()}_{self.timestamp}")

        self.is_running = True
        self.mainloop()

    def get_process_data(self):
        self.update_is_running()

        base_process_data = super().get_process_data()

        process_data = {
            **base_process_data,
            ProcessesConsts.OWNER_ID: self.user_id,
            ProcessesConsts.LOGS_SESSION_ID: self.logs_session_id,
            ProcessesConsts.SLEEPWALKING_DETECTED: self.detected
        }

        return process_data

    def get_body_logs(self):
        logs = models.BodySensorsLog.objects.filter(log_session__uuid=self.logs_session_id).all()

        return logs

    def mainloop(self):
        try:
            self.log_info(f"Starting {self.get_process_name()} for"
                          f" {self.user_id} and sessions {self.logs_session_id}")

            while self.is_running:
                self.update_process_data()

                self.get_body_logs()

                time.sleep(TasksDelays.SLEEPWALKING_DETECTION_DELAY)

        except Exception as e:
            self.log_error(str(e))

        finally:
            self.finish_process()
