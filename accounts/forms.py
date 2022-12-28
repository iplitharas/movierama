"""Accounts forms implementation"""
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class CustomUserCreationForm(
    UserCreationForm
):  # pylint: disable=missing-class-docstring
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("username", "email", "password1", "password2"):
            self.fields[field_name].help_text = ""


class CustomUserChangeForm(UserChangeForm):  # pylint: disable=missing-class-docstring
    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "username",
        )
