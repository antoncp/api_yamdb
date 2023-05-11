from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Genre model serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'

    def validate_name(self, value):
        """
        Check that the name field is unique (case insensetive).

        """
        value = value.capitalize()
        if Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                detail={'name': 'This genre already exists.'}
            )
        return value


class CategorySerializer(serializers.ModelSerializer):
    """Gategory model serializer."""

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_name(self, value):
        """
        Check that the name field is unique (case insensetive).

        """
        value = value.capitalize()
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                detail={'name': 'This category already exists.'}
            )
        return value


class TitleSerializer(serializers.ModelSerializer):
    """Title model serializer."""
    # genre = ...
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category')
        read_only_fields = ('id',)

    def to_representation(self, instance):
        """Add rating field."""
        representation = super().to_representation(instance)
        rating = instance.reviews.aggregate(Avg('score')).get('score__avg')
        representation['rating'] = round(rating) if rating else rating
        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """Review model serializer."""
    author = SlugRelatedField(
        slug_field="username",
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "title_id", "author", "pub_date")
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs['title_id']
        author = self.context["request"].user
        if Review.objects.filter(author=author, title_id_id=title_id).exists():
            raise serializers.ValidationError(
                'Only one review for one work from one author'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Comment model serializer."""
    author = SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "author", "pub_date")
        model = Comment
