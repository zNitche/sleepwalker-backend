from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from sleepwalker.apps.authenticate.forms import CustomUserCreationForm, CustomUserChangeForm
from sleepwalker.apps.authenticate.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ("username", "is_staff", "is_active")
    list_filter = ("username", "is_staff", "is_active")

    fieldsets = (
        ("Details", {
            "fields": ("username", "password", "date_joined", "api_key")
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "password1", "password2", "is_staff",
                "is_active"
            )}
         ),
    )

    search_fields = ("username",)
    ordering = ("username",)
    readonly_fields = ("date_joined",)


class AuthTokenAdmin(ModelAdmin):
    list_display = ("short_key", "creation_date", "expiration_date", "blacklisted", "is_expired", "user_id")
    search_fields = ("user_id", "key", "is_expired")

    readonly_fields = ["key", "creation_date", "expiration_date", "user_id"]
