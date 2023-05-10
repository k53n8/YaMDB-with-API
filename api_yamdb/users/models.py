from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    Admin = 'Admin'
    Moderator = 'Moderator'
    User = 'User'

    roles = [
        (Admin, 'Administrator'),
        (Moderator, 'Moderator'),
        (User, 'User'),
    ]

    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Псевдоним пользователя'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Информация о пользователе'
    )
    role = models.CharField(
        choices=roles,
        default=User,
        verbose_name='Роль'
    )

    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'