from rest_framework import serializers

from django.db.models import Avg


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий произведений."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров произведений."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class ShowTitlesSerializer(serializers.ModelSerializer):

    """Сериализатор для запросов к произведениям."""
    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(
        many=True
    )
    category = CategorySerializer()

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'genre', 'category'
        )
        model = Title

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score'))['score__avg']

        if rating is not None:
            rating = int(rating)

        return rating


class CreateUpdateTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для запросов к произведениям."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=True,
    )

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        required=False,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
