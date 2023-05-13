from django.conf import settings
from django.core.validators import MaxLengthValidator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import validate_username


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


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    username = serializers.CharField(
        validators=[MaxLengthValidator(settings.LIMIT_USERNAME),
                    validate_username]
    )
    email = serializers.EmailField(max_length=settings.LIMIT_EMAIL,
                                   required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    """Serializer for getting token."""

    username = serializers.CharField(
        validators=[MaxLengthValidator(settings.LIMIT_USERNAME),
                    validate_username]
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data['username']
        user = get_object_or_404(User, username=username)
        if user.confirmation_code != data['confirmation_code']:
            raise serializers.ValidationError('Confirmation code not correct.')
        return data


class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(
        validators=[MaxLengthValidator(settings.LIMIT_USERNAME)])

    last_name = serializers.CharField(
        validators=[MaxLengthValidator(settings.LIMIT_USERNAME)])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role'
                  )
