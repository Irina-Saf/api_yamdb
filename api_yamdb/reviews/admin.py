from django.contrib import admin

from .models import Category, Title, Genre, User


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'name',
        'year',
        'description',
        'category',
        # 'genre'
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",

    )

    empty_value_display = "-пусто-"


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
        'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
