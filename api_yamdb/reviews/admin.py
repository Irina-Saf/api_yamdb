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
    list_display = [
        'pk',
        'name',
        'year',
        'description',
        'category',
        # 'genre'

    ]


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",

    )

    empty_value_display = "-пусто-"


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio'

    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(User, UserAdmin)
