from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from auth.send_code import send_mail_with_code
from auth.get_token import get_tokens_for_user
from serializers import (ReviewSerializer, CommentSerializer,
                         AdminUserSerializer, UserSerializer,
                         GetTokenSerializer, SignUpSerializer)
from reviews.models import Title, Genre, Category, Comment, Review
from .serializers import (
    ReviewSerializer,
    CommentSerializer,
    AdminUserSerializer,
    UserSerializer,
    CategoriesSerializer,
    CreateUpdateTitleSerializer,
    GenresSerializer,
    ShowTitlesSerializer,
)
from reviews.models import Titles, Genres, Categories, Reviews
from .mixins import ListCreateDestroyViewSet
from users.models import User
from .permissions import (
    IsAdminModeratorOwnerOrReadOnly,
    AdminOrReadOnly,
    IsAdmin
)
from .filters import TitlesFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    Views отвечающий за работу c пользователями и настройку профиля.
    """
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ('username',)

    @action(
        detail=False, methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        serializer_class=UserSerializer,
        pagination_class=None
    )
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Views отвечающий за работу c отзывами к произведениям.
    """
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Views отвечающий за работу c комментариями к отзывам.
    """
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Reviews, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Reviews, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class APISignUp(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден.'},
                status=status.HTTP_404_NOT_FOUND)
        user.confirmation_code = send_mail_with_code(request.data)
        user.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
            username=serializer.validated_data['username'])
        token = get_tokens_for_user(user)
        return Response({'token': token},
                        status=status.HTTP_201_CREATED)

class CategoriesViewSet(ListCreateDestroyViewSet):
    """
    Views отвечающий за работу c категориями прoизведений.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenresViewSet(ListCreateDestroyViewSet):
    """
    Views отвечающий за работу c жанрами произведений.
    """
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    Views отвечающий за определенное произведение к которому пойдут отзывы.
    """
    queryset = Titles.objects.all()
    serializer_class = CreateUpdateTitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Переопределяем сериализатор"""
        if self.action in ['list', 'retrieve']:
            return ShowTitlesSerializer
        return CreateUpdateTitleSerializer
