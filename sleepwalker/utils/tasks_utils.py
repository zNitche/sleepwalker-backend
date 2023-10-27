from django.core.cache import cache
from django.conf import settings
from celery.result import AsyncResult
from sleepwalker.consts import ProcessesConsts


def read_from_cache(key):
    return cache.get(key)


def write_to_cache(key, value, timeout=None):
    cache.set(key, value, timeout)


def get_keys_by_pattern(pattern):
    keys = cache._cache.get_client().keys(pattern)
    cleared_keys = []

    for key in keys:
        cleared_keys.append(key.decode().split(":")[2])

    return cleared_keys


def get_key_by_pattern(pattern):
    keys = cache._cache.get_client().keys(pattern)
    cleared_keys = []

    for key in keys:
        cleared_keys.append(key.decode().split(":")[2])
        break

    return cleared_keys[0] if len(cleared_keys) > 0 else None


def get_tasks_keys_by_type(task_type):
    keys = get_keys_by_pattern(f"*{task_type}*")

    return keys


def get_tasks_keys_by_type_and_owner_id(task_type, owner_id):
    keys = get_keys_by_pattern(f"*{owner_id}_{task_type}*")

    return keys


def get_tasks_keys_by_type_and_owner_id_and_session_id(task_type, owner_id, session_id):
    keys = get_keys_by_pattern(f"*{owner_id}_{session_id}_{task_type}*")

    return keys


def get_task_data_by_key(key):
    data = cache.get(key)
    return data


def get_tasks_data_for_user(owner_id, task_type):
    keys = get_tasks_keys_by_type_and_owner_id(task_type, owner_id)
    data = [get_task_data_by_key(key) for key in keys]

    return data


def get_task_id(user_id, session_id, task_name):
    task_key = get_key_by_pattern(f"*{user_id}_{session_id}_{task_name}*")

    if task_key:
        task_data = get_task_data_by_key(task_key)
        return task_data.get(ProcessesConsts.TASK_ID)

    else:
        return None


def check_if_sleepwalking_detected_for_user(user_id):
    task_key = get_key_by_pattern(f"*{user_id}_*_SleepwalkingDetectionProcess*")

    if task_key:
        task_data = get_task_data_by_key(task_key)
        return task_data.get(ProcessesConsts.SLEEPWALKING_DETECTED, False)

    else:
        return False


def reset_sleepwalking_logger_for_user(user_id):
    task_key = get_key_by_pattern(f"*{user_id}_*_SleepwalkingDetectionProcess*")

    if task_key:
        task_data = get_task_data_by_key(task_key)
        task_data[ProcessesConsts.RESET_PROCESS] = True

        write_to_cache(task_key, task_data)


def run_task(task, params):
    if not settings.TESTING:
        task.apply_async(params)


def stop_task(user_id, session_id, task_name):
    if not settings.TESTING:
        tasks_keys = get_tasks_keys_by_type_and_owner_id_and_session_id(user_id, session_id, task_name)

        for key in tasks_keys:
            task_data = get_task_data_by_key(key)
            task_data[ProcessesConsts.IS_RUNNING] = False

            write_to_cache(key, task_data)


def force_stop_task_by_id(task_id):
    if not settings.TESTING and task_id is not None:
        task = AsyncResult(task_id)

        if task and not task.ready():
            task.revoke(terminate=True)
