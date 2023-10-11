from sleepwalker.celery_tasks.task_base import TaskBase
from sleepwalker.apps.authenticate import models
from sleepwalker.consts import TasksDelays, ProcessesConsts
import time


class SleepwalkingDetectionProcess(TaskBase):
    def __init__(self):
        super().__init__()

        self.user_id = None
        self.logs_session_id = None

        self.cache_data_timeout = 60

    def run(self, user_id, logs_session_id):
        self.user_id = user_id
        self.logs_session_id = logs_session_id
        self.process_cache_key = f"{self.user_id}_{self.logs_session_id}_{self.get_process_name()}_{self.timestamp}"

        self.is_running = True
        self.mainloop()

    def get_process_data(self):
        self.update_is_running()

        self.log_info(f"OwnerID: {self.user_id}, SessionID: {self.logs_session_id}, isRunning: {self.is_running}")

        process_data = {
            ProcessesConsts.OWNER_ID: self.user_id,
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
            ProcessesConsts.LOGS_SESSION_ID: self.logs_session_id,
            ProcessesConsts.IS_RUNNING: self.is_running
        }

        return process_data

    def mainloop(self):
        try:
            while self.is_running:
                self.update_process_data()

                self.log_info(f"OwnerID: {self.user_id}, SessionID: {self.logs_session_id}")

                time.sleep(TasksDelays.SLEEPWALKING_DETECTION_DELAY)

        except Exception as e:
            self.log_error(str(e))

        finally:
            self.finish_process()
