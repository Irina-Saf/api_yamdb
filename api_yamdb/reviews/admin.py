from django.contrib import admin

from .models import Category, Title, Genre, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'slug'
    )
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
        # 'genre'
    )
    search_fields = ('name',)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ('name',)
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


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
