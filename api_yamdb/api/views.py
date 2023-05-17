from random import sample
from string import hexdigits

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from api.filters import TitleFilter
from api.permissions import (
    IsAdminOnly, IsAdminOrReadOnly, IsOwnerAdminModeratorOrReadOnly,
)
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    SignUpSerializer, TitleSerializer, TokenSerializer, UserSerializer,
)


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GenreListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = ReviewSerializer

    def _get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerAdminModeratorOrReadOnly)
    serializer_class = CommentSerializer

    def _get_title(self):
        title_id = self.kwargs.get("title_id")
        return get_object_or_404(Title, id=title_id)

    def _get_review(self):
        review_id = self.kwargs.get("review_id")
        return get_object_or_404(Review, id=review_id)

    def get_queryset(self):
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        title = self._get_title()
        review = self._get_review()
        if review.title == title:
            serializer.save(author=self.request.user, review=review)


class SignUpViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Creates a new user and sends a confirmation code to email."""

    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (AllowAny,)

    def create_confirmation_code(self, user):
        """Create confirmation_code for registration."""

        confirmation_code = ''.join(sample(hexdigits, 6))
        user.confirmation_code = confirmation_code
        user.save()
        return confirmation_code

    def sent_confirmation_code(self, email, confirmation_code):
        subject = 'Registration in the YaMDb project.'
        message = f'Your confirmation code {confirmation_code}.'
        from_email = settings.ADMIN_EMAIL
        to_email = email
        return send_mail(subject, message, from_email, [to_email, ])

    def create(self, request):
        """."""
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = self.create_confirmation_code(user)
        self.sent_confirmation_code(email=user.email,
                                    confirmation_code=confirmation_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = serializer.data.get('confirmation_code')
    if confirmation_code == str(user.confirmation_code):
        return Response(f'token: {AccessToken.for_user(user)}',
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing users and editing user data."""

    lookup_field = 'username'
    queryset = User.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = UserSerializer
    permission_classes = (IsAdminOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated]
    )
    def me_page(self, request):
        """ViewSet for viewing by the user and
        editing information about himself."""

        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
