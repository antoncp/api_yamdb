from rest_framework import serializers

from reviews.models import Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Genre model serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_name(self, value):
        """
        Check that the name field is unique (case insensetive).

        """
        value = value.capitalize()
        if Genre.objects.filter(name=value).exists():
            raise serializers.ValidationError(
                detail={'name': 'Такой жанр уже есть.'}
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
                detail={'name': 'Такая категория уже есть.'}
            )
        return value
