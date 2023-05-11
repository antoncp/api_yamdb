from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        error_messages={
            'unique': 'This name is taken, please select another!',
        })

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
    bio = models.TextField(
        verbose_name='Biography',
        blank=True,
        max_length=250,
    )
    role = models.CharField(
        default=UserRoles.USER,
        choices=UserRoles.choices,
        max_length=12,
    )
    confirmation_code = models.CharField(
        verbose_name='Confirmation code',
        blank=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user',
            ),
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me")
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
        return self.username[:settings.STRING_OUTPUT_LENGTH]
