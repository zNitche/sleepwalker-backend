from sleepwalker.apps.logs_sessions import models
import datetime


def check_if_user_has_unfinished_session(user_id):
    sessions = models.LogsSession.objects.filter(user_id=user_id, end_date=None).all()

    return True if len(sessions) > 0 else False


def get_latest_sleepwalking_events_count(user_id, days_range=7):
    now_date = datetime.datetime.now()
    dates = [now_date - datetime.timedelta(days=date) for date in range(days_range)]
    struct = {}

    for date in dates:
        events_count = models.SleepwalkingEvent.objects.filter(user__id=user_id,
                                                               start_date__day=date.day,
                                                               start_date__month=date.month,
                                                               start_date__year=date.year,
                                                               ).count()

        struct[date.isoformat()] = events_count

    return struct
