from rest_framework import serializers

from reviews.models import Category, Title, Genre, User


# class TitleSerializer (serializers.ModelSerializer):
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#         many=True
#     )
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     # rating = serializers.IntegerField(required=False)

#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'rating',
#                   'description', 'category', 'genre')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


# class GenreSerializer(serializers.ModelSerializer):
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#     )

#     class Meta:
#         exclude = ('id',)
#         model = Genre
#         # lookup_field = 'slug'
#         # model = Genre
#         # fields = ('name', 'slug')
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


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
        fields = '__all__'
        model = Title


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        required=False
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category', 'rating'
                  )
        model = Title

# class CategorySerializer (serializers.Field):

#     class Meta:
#         model = Category
#         fields = ('name', 'slug')


# class GenreSerializer (serializers.Field):

#     class Meta:
#         model = Genre
#         fields = ('name', 'slug')
