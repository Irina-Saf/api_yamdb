from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, GetToken, Signup

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

api_users_pattern = [
    path('/auth/token/', GetToken.as_view(), name='get_token'),
    path('/auth/signup/', Signup.as_view(), name='signup'),
]
urlpatterns = [
    path('v1/', include(api_users_pattern)),
    path('v1/', include(router.urls)),
]