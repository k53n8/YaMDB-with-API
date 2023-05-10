from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Выберите категорию'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг'
    )

    def __str__(self):
        return self.slug

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

