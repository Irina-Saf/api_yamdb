from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_year


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
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(
        'Почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль пользователя',
        choices=ROLES,
        default=USER,
        max_length=20,
    )
    bio = models.TextField('Биография', blank=True)
    confirmation_code = models.CharField(
        'Код авторизации',
        max_length=255,
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
        max_length=256,
        verbose_name='Произведение'
    )
    year = models.IntegerField(
        validators=(validate_year,),
        verbose_name='Год выпуска произведения')

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
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        ordering = ('id',)

    def __str__(self):
        return f'{self.title} относится к жанру {self.genre}'


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts')
    score = models.IntegerField(validators=[MinValueValidator(1),
                                            MaxValueValidator(10)])
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviewing'
    )

    def __str__(self):
        return self.text

    class Meta:
        constraints = [UniqueConstraint(fields=['title', 'author', 'score'],
                       name='unique_rating')]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
