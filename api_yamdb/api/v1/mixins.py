from rest_framework import mixins, viewsets, filters

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
