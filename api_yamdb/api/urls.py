from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (UserViewSet, CategoriesViewSet, GenresViewSet,
                    TitlesViewSet, ReviewViewSet, CommentViewSet)

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register(r'categories', CategoriesViewSet, basename='categories')
v1_router.register(r'genres', GenresViewSet, basename='genres')
v1_router.register(r'titles', TitlesViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
