from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Title, Genre, User, Review, Comment
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer, CommentSerializer, ReviewSerializer)
from .filters import TitleFilter

from .permissions import (IsAuthorAdminModeratorOrReadOnly, IsAdmin,
                          IsAdminOrReadOnly)
from .serializers import (GetTokenSerializer, NotAdminSerializer,
                          SignUpSerializer, UserSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ('GET', 'POST', 'DELETE', 'PATH')

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_name='user_profile',
        url_path='me',
    )
    def personal_profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    permission_classes = (permissions.AllowAny,)

    def send_email(data, username):
        user = get_object_or_404(User, username=username)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject=f'Приветствуем вас, {user.username}.',
            message=f'Ваш код подверждения {confirmation_code}',
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False
        )

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        username = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        self.confirmation_code(username)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=request.data['username'])
        if data['confirmation_code'] == user.confirmation_code:
            refresh = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(refresh)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # Получаем id отзыва из эндпоинта
        title_id = self.kwargs.get('title_id')
        # И отбираем только нужные комментарии
        new_queryset = Review.objects.filter(title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=title)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super(ReviewViewSet, self).perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # queryset во вьюсете не указываем
    # Нам тут нужны не все комментарии,
    # а только связанные с отзывом id=review_id
    # Поэтому нужно переопределить метод get_queryset и применить фильтр

    def get_queryset(self):
        # Получаем id отзыва из эндпоинта
        review_id = self.kwargs.get('review_id')
        # И отбираем только нужные комментарии
        new_queryset = Comment.objects.filter(review=review_id)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
        super(CommentViewSet, self).perform_update(serializer)
