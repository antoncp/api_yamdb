from random import randint as create_code

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdminOrReadOnly, IsAdminOnly
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializer,
                             TokenSerializer, UserSerializer)
from api.filters import TitleFilter
from reviews.models import Category, Comment, Genre, Review, Title, User


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class GenreListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class CategoryListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAdminOrReadOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs["title_id"]
        return Review.objects.filter(title_id=title_id)

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title_id=title_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'title_id': self.kwargs.get('title_id')})
        return context


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs["title_id"]
        review_id = self.kwargs["review_id"]
        return Comment.objects.filter(title_id=title_id, review_id=review_id)

    def perform_create(self, serializer):
        title_id = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        review_id = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(
            author=self.request.user,
            title_id=title_id,
            review_id=review_id
        )


def create_confirmation_code(username):
    """Create and sent confirmation_code for registration."""

    confirmation_code = create_code(1000, 9999)
    user = get_object_or_404(User, username=username)
    user.confirmation_code = confirmation_code
    user.save()

    subject = 'Registration in the YaMDb project.'
    message = f'Your confirmation code {confirmation_code}.'
    from_email = settings.ADMIN_EMAIL
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Creates a new user and sends a confirmation code to email."""

    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    user = User.objects.filter(email=email)

    if user.exists():
        user = user.get(email=email)
        create_confirmation_code(user.username)
        return Response(
            {'message': 'User with this email exists.'
             'Verification code sent again.'
             },
            status=status.HTTP_400_BAD_REQUEST
        )

    else:
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        user = User.objects.get_or_create(username=username, email=email)
        create_confirmation_code(user)
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
