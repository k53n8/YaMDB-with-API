from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from users.models import User
from reviews.models import Title, Genre, Category, Comment, Review
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


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Title
    pass


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
    pass


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
    pass


class ReviewSerializer(serializers.ModelSerializer):
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
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise ValidationError(
                    'Вы уже оставили отзыв на это произведение!'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
