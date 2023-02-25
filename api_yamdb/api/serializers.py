import re

from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User


def validate_username(value):
    if (('username' in value and not re.compile(
            r'[\w.@+-]+$').match(value['username']))
            or ('username' in value and value['username'].lower() == 'me')):
        raise serializers.ValidationError('Недопустимое имя пользователя!')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        validators = (validate_username,)
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'bio',
            'role'
        )


class NotAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    confirmation_code = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        validators = (validate_username,)
        fields = ('email', 'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category',)
        model = Title


class TitleSerializer(serializers.ModelSerializer):

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.SerializerMethodField(
        required=False
    )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating'
                  )
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    author = SlugRelatedField(slug_field='username', read_only=True)

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError('Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Может существовать только один отзыв!')
        return data

    class Meta:
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['title', 'author', 'score'],
        #         message='Оценить можно только один раз!'
        #     )
        # ]
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')
