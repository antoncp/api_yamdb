from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.validators import validate_username


class UserRoles(models.TextChoices):
    """Roles for Custom User model."""

    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    """Custom User model."""

    username = models.CharField(
        _('username'), max_length=150, unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and '
                    '@/./+/-/_ only.'),
        validators=[RegexValidator(r'^[\w.@+-]+\Z',
                                   ('Enter a valid username. '
                                    'This value may contain only letters,'
                                    'numbers and @/./+/-/_ characters.'),
                                   'invalid'), validate_username],
        error_messages={
            'unique': _("A user with that username already exists."), })

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(max_length=settings.LIMIT_USERNAME,
                                  blank=True)

    last_name = models.CharField(max_length=settings.LIMIT_USERNAME,
                                 blank=True)

    bio = models.TextField(
        verbose_name='Biography',
        blank=True,
    )
    role = models.CharField(
        default=UserRoles.USER,
        choices=UserRoles.choices,
        max_length=12,
    )
    confirmation_code = models.CharField(
        verbose_name='Confirmation code',
        blank=True,
        max_length=50,
    )

    def clean(self):
        super().clean()
        if not self.password:
            self.password = None

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user',
            ),
        ]

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.username
