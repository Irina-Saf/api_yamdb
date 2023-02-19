from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Title, Genre, User, Comment, Review


class UserSerializer(serializers.ModelSerializer):

    class Meta:
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
        fields = ('username', 
                  'confirmation_code')


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 
                  'username')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('id',)


# class TitleCreateSerializer(serializers.ModelSerializer):
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#         many=True
#     )

#     class Meta:
#         fields = '__all__'
#         model = Title


# class TitleSerializer(serializers.ModelSerializer):
   
#     category = CategorySerializer(read_only=True)
#     genre = GenreSerializer(slug_field='slug',
#         queryset=Genre.objects.all(),
#         read_only=True, 
#         many=True)
#     rating = serializers.IntegerField(
#         required=False
#     )

#     class Meta:
#         fields = ('id', 'name', 'year',
#                   'description', 'genre', 'category', 'rating'
#                   )
#         model = Title

class TitleGETSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True,
                             read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class TitleSerializer(serializers.ModelSerializer):

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'name', 
            'year', 
            'rating',
            'description', 
            'genre', 
            'category')

    def to_representation(self, title):
        serializer = TitleGETSerializer(title)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['title', 'author', 'score'],
                message='Оценить можно только один раз!'
            )
        ]
        model = Review
        fields = '__all__'
