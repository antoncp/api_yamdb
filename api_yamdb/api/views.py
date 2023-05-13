from random import randint as create_code

from api.permissions import RoleIsAdmin
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializer,
                             TokenSerializer)
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
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

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (RoleIsAdmin,)
        return super().get_permissions()


class CategoryListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (RoleIsAdmin,)
        return super().get_permissions()


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


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


def send_confirmation_code(user):
    code = create_code(1000, 9999)
    user.confirmation_code = code
    user.save()

    subject = 'Registration in the YaMDb project.'
    message = f'Your confirmation code {code}.'
    from_email = settings.ADMIN_EMAIL
    to_email = [user.email]
    return send_mail(subject, message, from_email, to_email)


@api_view(['POST'])
def signup(request):
    """Creates a new user and sends a confirmation code to email."""

    serializer = SignUpSerializer(data=request.data)
    email = request.data.get('email')
    user = User.objects.filter(email=email)

    if user.exists():
        user = user.get(email=email)
        send_confirmation_code(user)
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
        send_confirmation_code(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    """Give a token to the user."""

    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        access = AccessToken.for_user(user)
        return Response(f'token: {access}', status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
