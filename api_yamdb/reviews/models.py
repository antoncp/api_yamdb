from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from reviews.validators import username_validator


class UserRoles(models.TextChoices):
    """Roles for Custom User model."""

    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    """Custom User model."""

    username = models.CharField(
        'Username',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        error_messages={
            'unique': 'This name is taken, please select another!',
        },
        validators=(username_validator,)
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )

    first_name = models.CharField(max_length=settings.LIMIT_USERNAME,
                                  blank=True)

    last_name = models.CharField(max_length=settings.LIMIT_USERNAME,
                                 blank=True)

    bio = models.TextField(
        verbose_name='Biography',
        blank=True,
        max_length=250,
    )
    role = models.CharField(
        default=UserRoles.USER,
        choices=UserRoles.choices,
        max_length=12,
    )
    confirmation_code = models.CharField(
        verbose_name='Confirmation code',
        blank=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_user',
            ),
        ]

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.username


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
        related_query_name='titles'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='Category',
        related_query_name='titles',
        null=True,
    )

    class Meta:
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year', 'category'],
                name='name_year_category'
            )
        ]

    def __str__(self):
        return f'{self.category} "{self.name}", {self.year}'

    def display_genres(self):
        return ', '.join(map(str, self.genre.all()))

    display_genres.short_description = 'Genres'


class Review(models.Model):
    """Review db model class."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Author",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Work",
    )
    text = models.TextField(verbose_name="Text")
    score = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name="Score"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date created"
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="only_one_review_allowed"
            ),
        ]

    def __str__(self):
        return self.text[:settings.STRING_OUTPUT_LENGTH]


class Comment(models.Model):
    """Comment db model class."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Author",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Work",
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Review",
    )
    text = models.TextField(verbose_name="Comment")
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date created"
    )

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.text[:settings.STRING_OUTPUT_LENGTH]
