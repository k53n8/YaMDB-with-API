from .mixins import ListCreateDestroyViewSet
from .serializers import (
    CategorySerializer,
    CreateUpdateTitleSerializer,
    GenreSerializer,
    ShowTitlesSerializer,

)


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = CreateUpdateTitleSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ShowTitlesSerializer
        return CreateUpdateTitleSerializer
