from django.core.validators import RegexValidator

username_validator = RegexValidator(
    regex=r'^[\w.@+-]+\z',
    message='Username should contain only letters, digits,'
    'and the following characters: @ . + - ',
    code='invalid_username'
)
