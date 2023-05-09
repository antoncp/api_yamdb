from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


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
    text = models.TextField(verbose_name="Text of review")
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
        verbose_name="Score"
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date of creation"
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title_id"], name="Only one review allowed"
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
