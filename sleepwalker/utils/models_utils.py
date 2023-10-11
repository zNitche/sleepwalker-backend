from sleepwalker.apps.logs_sessions import models


def check_if_user_has_unfinished_session(user_id):
    sessions = models.LogsSession.objects.filter(user_id=user_id, end_date=None).all()

    return True if len(sessions) > 0 else False
