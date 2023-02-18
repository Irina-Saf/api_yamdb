from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, GetToken, Signup, CategoryViewSet, TitleViewSet, GenreViewSet, ReviewViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'users/', UserViewSet, basename='users')
router.register(r'categories/', CategoryViewSet, basename='category')
router.register(r'genres/', GenreViewSet, basename='genre')
router.register(r'titles/', TitleViewSet, basename='title')
router.register(r'titles/(?P<title_id>/reviews', ReviewViewSet)
router.register(r'titles/(?P<title_id>/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='comments')


api_users_pattern = [
    path('/auth/token/', GetToken.as_view(), name='get_token'),
    path('/auth/signup/', Signup.as_view(), name='signup'),
]
urlpatterns = [
    path('', include(router.urls)),
    path('', include(api_users_pattern))
]