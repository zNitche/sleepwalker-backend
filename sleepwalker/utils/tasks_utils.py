from django.core.cache import cache
from django.conf import settings
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
