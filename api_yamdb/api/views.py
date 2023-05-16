from django.db import IntegrityError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, status, filters
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated, AllowAny)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.get_token import get_user_token
from authentication.send_confirmation import send_mail_with_code
from reviews.models import Title, Genre, Category, Review
from users.models import User
from .serializers import (ReviewSerializer, CommentSerializer,
                          UserSerializer, ShowTitlesSerializer,
                          GetTokenSerializer, SignUpSerializer,
                          CategoriesSerializer, CreateUpdateTitleSerializer,
                          GenresSerializer, UserPatchSerializer)
from .mixins import ListCreateDestroyViewSet
from .permissions import (IsAdmin,
                          IsAdminModeratorOwnerOrReadOnly,
                          AdminOrReadOnly)
from .filters import TitlesFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    View отвечающий за работу c пользователями и настройку профиля.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin, IsAuthenticatedOrReadOnly)
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
    )
    def me(self, request):
        user = get_object_or_404(User,
                                 username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserPatchSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    View отвечающий за работу c отзывами к произведениям.
    """
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    View отвечающий за работу c комментариями к отзывам.
    """
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class APISignUp(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            User.objects.get_or_create(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email'))
        except IntegrityError:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        send_mail_with_code(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIGetToken(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        data = request.data
        serializer = GetTokenSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=data.get('username'))
        token = get_user_token(user)
        confirmation_code = data['confirmation_code']
        if not default_token_generator.check_token(
                user,
                confirmation_code
        ):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'token': token},
                        status=status.HTTP_201_CREATED)


class CategoriesViewSet(ListCreateDestroyViewSet):
    """
    View отвечающий за работу c категориями прoизведений.
    """
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class GenresViewSet(ListCreateDestroyViewSet):
    """
    View отвечающий за работу c жанрами произведений.
    """
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    """
    View отвечающий за определенное произведение к которому пойдут отзывы.
    """
    queryset = Title.objects.all()
    serializer_class = CreateUpdateTitleSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter

    def get_serializer_class(self):
        """Переопределяем сериализатор"""
        if self.action in ['list', 'retrieve']:
            return ShowTitlesSerializer
        return CreateUpdateTitleSerializer
