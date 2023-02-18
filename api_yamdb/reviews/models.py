from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
        (USER, 'Пользователь'),
    ]

    username = models.CharField(
        'Имя пользователя',
        max_length=50,
        unique=True,
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        'Почта',
        max_length=150,
        unique=True,
    )
    role = models.CharField(
        'Роль пользователя',
        choices=ROLES,
        default=USER,
        max_length=50,
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_fields'
            )
        ]

class Category(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Категория',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Жанр произведения'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        db_index=True,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Произведение'
    )
    year = models.IntegerField(verbose_name='Год выпуска произведения')
    rating = models.IntegerField(verbose_name='Рейтинг произведения')
    description = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

