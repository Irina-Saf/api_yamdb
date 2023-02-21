from django_filters.rest_framework import DjangoFilterBackend
import uuid
# from django.db.models import Avg
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Category, Title, Genre, User, Review, Comment
from .serializers import (TitleSerializer, GenreSerializer, CategorySerializer,
                          CommentSerializer, ReviewSerializer)
from .filters import TitleFilter

from .permissions import (IsAuthorAdminModeratorOrReadOnly, IsAdmin,
                          IsAdminOrReadOnly)
from .serializers import (GetTokenSerializer, SignUpSerializer,
                          UserSerializer, NotAdminSerializer, TitleCreateSerializer)
from .mixins import CreateListDestroyViewSet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )
    http_method_names = ['post', 'get', 'patch', 'delete']

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
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )

            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = NotAdminSerializer(
                request.user,
                data=request.data,
                partial=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(APIView):
    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class Signup(APIView):
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        confirmation_code = str(uuid.uuid4())
        data = {
            'email_body': (
                f'Приветствуем вас, {username}.'
                f'\nВаш код подверждения : {confirmation_code}'
            ),
            'to_email': email,
            'email_subject': 'Ваш код подверждения'
        }
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            if user.email != email:
                return Response(
                    {'error': ('Несоответствие Email адреса.')},
                    status=status.HTTP_400_BAD_REQUEST)
            serializer = SignUpSerializer(user, data=request.data)
        else:
            serializer = SignUpSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data['email_body'] = data['email_body'].format(
            confirmation_code=user.confirmation_code)
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    # queryset = Title.objects.all().annotate(
    #     rating=Avg('reviews__score')).order_by('-id')
    # pagination_class = LimitOffsetPagination
    # permission_classes = [IsAdminOrReadOnly]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination


class GenreViewSet(CreateListDestroyViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
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
    permission_classes = (IsAuthorAdminModeratorOrReadOnly,)
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
