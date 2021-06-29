import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


def max_value_current_year(value):
    """
    Return current year in MaxValueValidator format for Title model

    :rtype: object
    """
    current_year = datetime.date.today().year
    return MaxValueValidator(current_year)(value)


class Category(models.Model):
    """
    Stores a single category
    """
    name = models.CharField(verbose_name='Название категории', max_length=200)
    slug = models.SlugField(
        unique=True, max_length=300, verbose_name='category_slug'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('id',)

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    """
    Stores a single category, related to :model:`Category` and :model:`Genre`
    """
    name = models.CharField(
        verbose_name='Название произведения', max_length=200
    )
    year = models.PositiveIntegerField(
        blank=True,
        validators=[MinValueValidator(1500), max_value_current_year],
        verbose_name='title_year',
    )
    description = models.TextField(
        blank=True, verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        related_name='category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Описание кагетории',
    )
    genre = models.ManyToManyField(
        'Genre',
        related_name='genre',
        blank=True,
        verbose_name='Жанр произведения',
    )

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    """
    Stores a single genre
    """
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True, max_length=300, verbose_name='Слаг')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name[:15]


class Review(models.Model):
    """
    A class to represent Review for Title
    """
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rewiew',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата отзыва',
        auto_now_add=True,
        help_text='Хранится дата отзыва',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_together'
            )
        ]
        ordering = ('id',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """
    A class to represent Comment for Reviews
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Отзыв',
    )
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        help_text='Хранится дата комментария',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]
