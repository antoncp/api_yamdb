from django.core.exceptions import ValidationError
from django.conf import settings


def validate_username(value):
    """Validate that username value is allowed."""
    if value in settings.FORBIDDEN_USERNAMES:
        raise ValidationError(
            f'The username {value} is not allowed.'
        )
