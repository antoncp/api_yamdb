from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleSerializer)
from api.permissions import RoleIsAdmin
from reviews.models import Category, Comment, Genre, Review, Title


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
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ['category', 'genre', 'year', 'name']   # надо добавить кастомный фильтр по слагам
    permission_classes = (AllowAny,)
    serializer_class = TitleSerializer


"""
    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = (RoleIsAdmin,)
        return super().get_permissions()

"""


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


def signup():
    pass


def get_token():
    pass
