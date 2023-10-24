import celery
import logging
from django.conf import settings
from django.core.cache import cache
from datetime import datetime
from sleepwalker.consts import ProcessesConsts


class TaskBase(celery.Task):
    def __init__(self):
        self.is_running = False
        self.timestamp = str(datetime.timestamp(datetime.now()))

        self.process_cache_key = f"{self.get_process_name()}_{self.timestamp}"
        self.cache_data_timeout = 30

        self.logger = logging.getLogger(settings.CELERY_LOGGER_NAME)

    def get_process_name(self):
        return type(self).__name__

    def run(self, *args, **kwargs):
        self.is_running = True
        self.mainloop()

    def mainloop(self):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def save_to_cache(self, key, value):
        cache.set(key, value, self.cache_data_timeout)

    def read_from_cache(self, key):
        return cache.get(key)

    def clear_process_cache_entry(self, key):
        cache.delete(key)

    def finish_process(self):
        self.is_running = False
        self.clear_process_cache_entry(self.process_cache_key)

    def update_is_running(self):
        process_data = self.read_from_cache(self.process_cache_key)

        if process_data:
            self.is_running = True if process_data.get(ProcessesConsts.IS_RUNNING) else False

    def get_process_data(self):
        process_data = {
            ProcessesConsts.PROCESS_NAME: self.get_process_name(),
            ProcessesConsts.PROCESS_TIMESTAMP: self.timestamp,
            ProcessesConsts.IS_RUNNING: self.is_running,
            ProcessesConsts.TASK_ID: self.request.id
        }

        return process_data

    def update_process_data(self):
        process_data = self.get_process_data()
        self.save_to_cache(self.process_cache_key, process_data)

    def log_info(self, message):
        self.logger.info(f"[{self.get_process_name()}] - {message}")

    def log_debug(self, message):
        self.logger.debug(f"[{self.get_process_name()}] - {message}")

    def log_error(self, message):
        self.logger.error(f"[{self.get_process_name()}] - {message}")

    def check_if_same_task_running(self):
        running_processes = 0
        workers = self.app.control.inspect().active()

        for worker in workers:
            for task in workers[worker]:
                if self.get_process_name() in task["name"]:
                    running_processes += 1

        running = True if running_processes > 1 else False

        return running
