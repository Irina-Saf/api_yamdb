from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    bio = models.TextField('Биография', blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    name = models.TextField(
        max_length=256,
        verbose_name='Категория произведения'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(verbose_name='Год выпуска произведения')
    rating = models.IntegerField(verbose_name='Рейтинг произведения')
    description = models.TextField(verbose_name='Описание произведения')
    category = models.OneToOneField(
        Category,
        on_delete=models.PROTECT,
        primary_key=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

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
        verbose_name='Тег'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
