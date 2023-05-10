from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Category, Genre, Title


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
