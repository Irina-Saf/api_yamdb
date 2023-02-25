from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import UniqueConstraint

from .validators import validate_year, validate_genry_null


ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLES = [
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER),
]

MINSCOREVALUE = 1
MAXSCOREVALUE = 10


class User(AbstractUser):

    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    email = models.EmailField(
        verbose_name='Email пользователя',
        max_length=254,
        unique=True
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLES,
        default=USER,
        max_length=20,
    )
    bio = models.TextField(verbose_name='Биография', blank=True)
    confirmation_code = models.CharField(
        verbose_name='Код авторизации',
        max_length=255,
        blank=True,
        default='QWERTY'
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user'
            )
        ]

    def __str__(self):
        return self.username


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    name = models.TextField(
        max_length=256,
        unique=True,
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
        verbose_name='Произведение',
        help_text='Укажите произведение'
    )
    year = models.PositiveSmallIntegerField(
        validators=(validate_year,),
        verbose_name='Год создания',
        help_text='Укажите год создания произведения'
    )
    description = models.TextField(
        max_length=200,
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        max_length=200,
        blank=True,
        null=True,
        related_name='titles',
        help_text='Укажите категорию',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        # validators=(validate_genry_null,),
        related_name='titles',
        help_text='Укажите жанр',
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
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(validators=(
                                             MinValueValidator(MINSCOREVALUE),
                                             MaxValueValidator(MAXSCOREVALUE)))
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Отзывы на произведения'
        ordering = ('title',)
        constraints = [UniqueConstraint(fields=['author', 'title'],
                       name='unique_rating')]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Комментарий {self.text} к отзыву {self.review}'

    class Meta:
        verbose_name = 'Комментарии к отзывам'
        ordering = ('review',)
