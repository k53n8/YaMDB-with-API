from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Avg

from users.models import User
from reviews.models import Titles, Genres, Categories, Comments, Reviews
from .validators import UsernameMinSymbolLimit


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для эндпойнта /users/,
    используется админом
    """
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            UsernameMinSymbolLimit
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        ordering = ['username']
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для эндпойнта /users/me,
    используется пользователем
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('username', 'email', 'role')


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Categories
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        model = Genres
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class ShowTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к произведениям."""

    rating = serializers.SerializerMethodField()
    genre = GenresSerializer(
        many=True
    )
    category = CategoriesSerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Titles

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']

        if rating is not None:
            rating = int(rating)

        return rating


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к произведениям."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all(),
        required=True,
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genres.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к отзывам."""
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        title_id = request.parser_context['kwargs'].get('title_id')
        title = get_object_or_404(Titles, pk=title_id)
        if request.method == 'POST':
            if Reviews.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    'Вы уже оставили отзыв на это произведение!'
                )
        return data

    class Meta:
        model = Reviews
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к комментариям."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comments
        fields = ('id', 'text', 'author', 'pub_date')
