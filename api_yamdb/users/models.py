from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator


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
        max_length=20,
        unique=True,
        verbose_name='Псевдоним пользователя',
        validators=[UnicodeUsernameValidator, ]
    )
    email = models.EmailField(
        unique=True,
        max_length=75
    )
    role = models.SlugField(
        choices=roles,
        default=User,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Информация о пользователе'
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
