from django.db import models
from django.core.exceptions import ValidationError


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
