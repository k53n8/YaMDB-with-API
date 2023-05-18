from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, CategoriesViewSet, GenresViewSet, APIGetToken,
                    APISignUp, TitlesViewSet, ReviewViewSet, CommentViewSet)

v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoriesViewSet, basename='categories')
v1_router.register('genres', GenresViewSet, basename='genres')
v1_router.register('titles', TitlesViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   '/comments', CommentViewSet, basename='comments')

auth_urls = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignUp.as_view(), name='signup')
]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('', include(v1_router.urls)),
]
