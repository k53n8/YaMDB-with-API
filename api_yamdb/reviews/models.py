from django.db import models
from django.conf import settings
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from users.models import User
from api.v1.validators import year_validation


class Category(models.Model):
    name = models.CharField(
        max_length=settings.NAME_SYM_LIMIT,
        verbose_name='Название категории',
        db_index=True
    )
    slug = models.SlugField(
        max_length=settings.SLUG_SYM_LIMIT,
        unique=True,
        verbose_name='Слаг',
        validators=[
            RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=settings.NAME_SYM_LIMIT,
        verbose_name='Название жанра',
        db_index=True
    )
    slug = models.SlugField(
        max_length=settings.SLUG_SYM_LIMIT,
        unique=True,
        verbose_name='Слаг',
        validators=[
            RegexValidator(regex=r'^[-a-zA-Z0-9_]+$')]
    )

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=settings.NAME_SYM_LIMIT,
        verbose_name='Наименование произведения'
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[year_validation]
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')

    class Meta:
        ordering = ['name']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1, 'Значение должно быть от 1 до 10!'),
            MaxValueValidator(10, 'Значение должно быть от 1 до 10!')
        ],
        verbose_name='Рейтинг'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            ),
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.SYMBOL_LIMIT]
