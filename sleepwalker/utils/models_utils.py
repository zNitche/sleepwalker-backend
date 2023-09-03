from django.conf import settings
import datetime
import secrets
import uuid


def generate_token():
    return secrets.token_hex(128)


def get_token_expiration_date():
    return datetime.datetime.utcnow() + settings.API_AUTH_TOKEN_LIFESPAN


def generate_uuid():
    return uuid.uuid4().hex
