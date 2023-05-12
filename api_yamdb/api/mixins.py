from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):

    pass
