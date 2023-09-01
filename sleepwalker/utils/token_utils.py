from django.conf import settings
import datetime
import secrets


def generate_token():
    return secrets.token_hex(128)


def get_token_expiration_date():
    return datetime.datetime.utcnow() + settings.API_AUTH_TOKEN_LIFESPAN
