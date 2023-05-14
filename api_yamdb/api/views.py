from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.get_token import get_user_token
from authentication.send_confirmation import send_mail_with_code

from .serializers import (ReviewSerializer, CommentSerializer,
                          AdminUserSerializer, UserSerializer,
                          GetTokenSerializer, SignUpSerializer)

from reviews.models import Title, Review
from users.models import User
from .permissions import IsAdmin, IsAdminOrAuthor


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
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
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrAuthor)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrAuthor)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id, title=title_id)
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
        token = get_user_token(user)
        return Response({'token': token},
                        status=status.HTTP_201_CREATED)
