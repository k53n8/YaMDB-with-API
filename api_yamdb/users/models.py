from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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
        max_length=150,
        unique=True,
        verbose_name='Псевдоним пользователя',
        validators=[
            RegexValidator(regex=r'^[\w@.+-_]+$')
        ]
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
        blank=True
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
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
