from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils import timezone


class GroupBaseModel(models.Model):
    """Group abstract model."""
    is_cleaned = False

    name = models.CharField(
        'Название',
        max_length=256,
        unique=True,
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def clean(self):
        self.is_cleaned = True
        if self.__class__.objects.filter(name=self.name.capitalize()).exists():
            raise ValidationError('Такое название уже есть в базе данных.')

    def save(self, *args, **kwargs):
        """Save all names in uppercase format for consistency."""
        if not self.is_cleaned:
            self.full_clean()
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class Genre(GroupBaseModel):
    """Genre db model class."""

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Category(GroupBaseModel):
    """Category db model class."""

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Title(models.Model):
    """Title db model class."""
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
    )
    genres = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_query_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        related_query_name='titles',
        null=True,
    )

    def display_genres(self):
        return ', '.join(map(str, self.genres.all()))

    display_genres.short_description = 'Жанры'
