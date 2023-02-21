from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (UserViewSet, GetToken, Signup, CategoryViewSet,
                    TitleViewSet, GenreViewSet, ReviewViewSet, CommentViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'titles', TitleViewSet, basename='title')
# router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet)
# router.register(r'titles/(?P<title_id>\d+)/reviews/'
#                 r'(?P<review_id>\d+)/comments',
#                 CommentViewSet, basename='comments')

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='title_id'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='review_id')


api_users_pattern = [
    path('auth/token/', GetToken.as_view()),
    path('auth/signup/', Signup.as_view()),
]
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(api_users_pattern)),
    # path('auth/', include('djoser.urls')),
    # # JWT-эндпоинты, для управления JWT-токенами:
    # path('auth/', include('djoser.urls.jwt')),

]
