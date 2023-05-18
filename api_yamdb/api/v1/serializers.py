from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from django.conf import settings

from users.models import User
from reviews.models import Title, Genre, Category, Comment, Review
from .validators import me_forbidden


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для работы с пользователями.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')


class UserPatchSerializer(serializers.ModelSerializer):
    """
    Сериализатор для редактирования профиля.
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name',
                  'bio', 'role')
        read_only_fields = ('role',)


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""
    class Meta:
        model = Category
        exclude = ('id',)


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""
    class Meta:
        model = Genre
        exclude = ('id',)


class ShowTitlesSerializer(serializers.ModelSerializer):
    """Сериализатор для GET запросов к произведениям."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenresSerializer(many=True)
    category = CategoriesSerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для небезопасных запросов к произведениям."""
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    rating = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        serializer = ShowTitlesSerializer(instance)
        return serializer.data

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к отзывам."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            title_id = request.parser_context['kwargs'].get('title_id')
            title = get_object_or_404(Title, pk=title_id)
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
    """Сериализатор для запросов к комментариям."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.NAME_SYM_LIMIT,
        validators=[
            me_forbidden,
            RegexValidator(regex=r'^[\w@.+-_]+$')
        ]
    )
    confirmation_code = serializers.CharField()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_SYM_LIMIT,
        required=True,
        validators=[
            me_forbidden,
            RegexValidator(regex=r'^[\w@.+-_]+$')
        ]
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_SYM_LIMIT,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email')
