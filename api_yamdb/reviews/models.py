from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils import timezone


class GroupBaseModel(models.Model):
    """Group abstract model."""
    is_cleaned = False

    name = models.CharField(
        'Name',
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
            raise ValidationError('This name already exists.')

    def save(self, *args, **kwargs):
        """Capitalize all names before saving for consistency."""
        if not self.is_cleaned:
            self.full_clean()
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class Genre(GroupBaseModel):
    """Genre db model class."""

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"


class Category(GroupBaseModel):
    """Category db model class."""

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Title(models.Model):
    """Title db model class."""
    name = models.CharField(
        'Name',
        max_length=256,
    )
    year = models.PositiveSmallIntegerField(
        'Release year',
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.TextField(
        'Description',
        null=True,
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Genre',
        related_query_name='Genres'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        verbose_name='Category',
        related_query_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = "Work of art"
        verbose_name_plural = "Works of art"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='name_year_category'
            )
        ]

    def __str__(self):
        return self.name

    def display_genres(self):
        return ', '.join(map(str, self.genre.all()))

    display_genres.short_description = 'Genres'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    score = models.SmallIntegerField()
