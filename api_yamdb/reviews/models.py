from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserRoles(models.TextChoices):
    USER = 'user', _('User')
    MODERATOR = 'moderator', _('Moderator')
    ADMIN = 'admin', _('Admin')


class User(AbstractUser):
    username = models.CharField(
        'Username',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        error_messages={
            'unique': 'This name is taken, please select another!',
        })

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
    )
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
            models.CheckConstraint(
                check=~models.Q(username="me"), name="name_not_me")
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
        return self.username[:settings.STRING_OUTPUT_LENGTH]


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
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Work",
    )
    text = models.TextField(verbose_name="Text")
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name="Score"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date created"
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title_id"], name="only_one_review_allowed"
            ),
        ]


class Comment(models.Model):
    """Comment db model class."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Author",
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Work",
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Review",
    )
    text = models.TextField(verbose_name="Comment")
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date of creation"
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

