from django.conf import settings
import datetime
import secrets
import uuid


def generate_token(nbytes_length=128):
    return secrets.token_hex(nbytes_length)


def generate_api_key():
    return generate_token(8)


def get_token_expiration_date():
    return datetime.datetime.utcnow() + settings.API_AUTH_TOKEN_LIFESPAN


def generate_uuid():
    return uuid.uuid4().hex
