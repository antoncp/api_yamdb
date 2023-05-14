from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

username_validator = RegexValidator(
    regex=r'^[\\w.@+-]+\\z',
    message='Username should contain only letters, digits,'
    'and the following characters: @ . + - ',
    code='invalid_username'
)


def validate_username(value):
    if value == 'me':
        raise ValidationError('Username cannot be "me"')