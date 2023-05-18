from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

from api.v1.validators import me_forbidden, username_symbols


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLES = [
        (ADMIN, 'administrator'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]

    username = models.CharField(
        max_length=settings.USERNAME_SYM_LIMIT,
        unique=True,
        verbose_name='Псевдоним пользователя',
        validators=[
            me_forbidden,
            username_symbols
        ]
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.SlugField(
        choices=ROLES,
        default=USER,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Информация о пользователе'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
