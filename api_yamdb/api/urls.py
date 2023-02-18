from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, GetToken, Signup, CategoryViewSet, TitleViewSet, GenreViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='category')
router_v1.register('genres', GenreViewSet, basename='genre')
router_v1.register('titles', TitleViewSet, basename='title')


urlpatterns = [
    path('v1/', include(router_v1.urls))
]

api_users_pattern = [
    path('/auth/token/', GetToken.as_view(), name='get_token'),
    path('/auth/signup/', Signup.as_view(), name='signup'),
]
urlpatterns = [
    path('v1/', include(api_users_pattern)),
    path('v1/', include(router_v1.urls)),
]