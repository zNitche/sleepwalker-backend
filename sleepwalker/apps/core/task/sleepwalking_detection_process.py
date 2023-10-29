from sleepwalker.celery_tasks.task_base import TaskBase
from sleepwalker.consts import TasksDelays, ProcessesConsts
from sleepwalker.apps.logs_sessions import models
import time
import statistics


class SleepwalkingDetectionProcess(TaskBase):
    def __init__(self):
        super().__init__()

        self.cache_data_timeout = 60
        self.extra_delay = 0

        self.user_id = None
        self.logs_session_id = None
        self.hb_percentage_threshold = None

        self.detected = False
        self.seconds_per_log = 2

        self.body_logs_per_long_segment = 600 * self.seconds_per_log
        self.body_logs_per_short_segment = 8 * self.seconds_per_log
        self.body_logs_offset = 0

        self.body_logs_event_detected = False

        self.body_logs_data = {
            "hb_mean_long": 0,
            "hb_mean_short": 0
        }

    def run(self, user, logs_session_id):
        self.user_id = user.id
        self.hb_percentage_threshold = user.settings.sw_detection_heart_beat_percentage_threshold
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

    def get_body_logs_queryset(self):
        return models.BodySensorsLog.objects.filter(
            log_session__uuid=self.logs_session_id).order_by("-date")

    def get_body_logs(self, limit=30, offset=None):
        body_sensors_logs_queryset = self.get_body_logs_queryset()

        if offset is not None:
            logs = body_sensors_logs_queryset[offset:offset + limit]
        else:
            logs = body_sensors_logs_queryset[:limit]

        return logs

    def get_body_logs_count(self):
        body_sensors_logs_queryset = self.get_body_logs_queryset()

        return body_sensors_logs_queryset.count()

    def process_body_logs_short_mean(self):
        logs = self.get_body_logs(limit=self.body_logs_per_short_segment)

        if len(logs) >= self.body_logs_per_short_segment:
            heart_beat_values = [log.heart_beat for log in logs]
            self.body_logs_data["hb_mean_short"] = round(statistics.mean(heart_beat_values), 2)

    def process_body_logs_long_mean(self):
        logs = self.get_body_logs(limit=self.body_logs_per_long_segment, offset=self.body_logs_offset)

        if len(logs) == self.body_logs_per_long_segment:
            self.body_logs_offset += self.body_logs_per_long_segment

            heart_beat_values = [log.heart_beat for log in self.get_body_logs(self.body_logs_per_long_segment)]
            self.body_logs_data["hb_mean_long"] = round(statistics.mean(heart_beat_values), 2)

    def process_body_logs(self):
        self.process_body_logs_long_mean()
        self.process_body_logs_short_mean()

        hb_mean_long = self.body_logs_data["hb_mean_long"]
        hb_mean_short = self.body_logs_data["hb_mean_short"]

        if hb_mean_long > 0:
            long_threshold = hb_mean_long + ((hb_mean_long / 100) * self.hb_percentage_threshold)

            if hb_mean_short >= long_threshold:
                self.body_logs_event_detected = True

    def check_sleepwalking(self):
        detection = self.body_logs_event_detected

        if self.detected != detection:
            self.detected = detection
            self.update_process_data()

    def handle_process_data_after_reset(self):
        self.body_logs_data["hb_mean_long"] = 0
        self.body_logs_data["hb_mean_short"] = 0

        self.detected = False
        self.body_logs_event_detected = False
        self.extra_delay = TasksDelays.SLEEPWALKING_DETECTION_RESET_EXTRA_DELAY

    def mainloop(self):
        try:
            self.log_info(f"Starting {self.get_process_name()} for"
                          f" {self.user_id} and sessions {self.logs_session_id} | {self.request.id}")

            while self.is_running:
                self.check_process_reset_request()
                self.update_process_data()

                self.process_body_logs()
                self.check_sleepwalking()

                delay = TasksDelays.SLEEPWALKING_DETECTION_DELAY
                if self.extra_delay > 0:
                    delay += self.extra_delay
                    self.extra_delay = 0

                time.sleep(delay)

        except Exception as e:
            self.log_error(str(e))

        finally:
            self.finish_process()
