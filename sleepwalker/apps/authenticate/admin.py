from django.contrib import admin
from sleepwalker.apps.authenticate.models import User, AuthToken
from sleepwalker.apps.authenticate import admin_models


# Register your models here.
admin.site.register(User, admin_models.CustomUserAdmin)
admin.site.register(AuthToken, admin_models.AuthTokenAdmin)
