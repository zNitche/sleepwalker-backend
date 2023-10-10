import celery
import logging
from django.conf import settings
from django.core.cache import cache


class TaskBase(celery.Task):
    def __init__(self):
        self.logger = logging.getLogger(settings.CELERY_LOGGER_NAME)
        self.is_running = False

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
        cache.set(key, value)

    def read_from_cache(self, key):
        return cache.get(key)

    def clear_process_cache_entry(self, key):
        cache.delete(key)

    def check_if_same_task_running(self):
        running_processes = 0
        workers = self.app.control.inspect().active()

        for worker in workers:
            for task in workers[worker]:
                if self.get_process_name() in task["name"]:
                    running_processes += 1

        running = True if running_processes > 1 else False

        return running
