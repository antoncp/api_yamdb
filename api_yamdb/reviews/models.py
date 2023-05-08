from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )

    username = models.CharField(
        "Имя пользователя",
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        error_messages={
            "unique": "Это имя занято, выберите другое!",
        })

    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True,
        max_length=254,
    )
    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        max_length=250,
    )
    role = models.CharField(
        verbose_name='Роль',
        default='user',
        choices=ROLES,
        max_length=12,
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        blank=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
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
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    def __str__(self):
        return self.username[:15]
