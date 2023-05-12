from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategoriesSerializer,
    CreateUpdateTitleSerializer,
    GenresSerializer,
    ShowTitlesSerializer,

)


class CategoriesViewSet(ListCreateDestroyViewSet):
    """
    Views отвечающий за работу c категориями прoизведений.
    """

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)


class GenresViewSet(ListCreateDestroyViewSet):
    """
    Views отвечающий за работу c жанрами произведений.
    """

    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)

class TitleViewSet(viewsets.ModelViewSet):
    """
    Views отвечающий за определенное произведение к которому пойдут отзывы.
    """

    queryset = Title.objects.all()
    serializer_class = CreateUpdateTitleSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        """Переопределяем сериализатор"""
        if self.action in ['list', 'retrieve']:
            return ShowTitlesSerializer

        return CreateUpdateTitleSerializer
