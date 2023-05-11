from rest_framework import viewsets
from rest_framework import mixins

from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer)
from reviews.models import Category, Genre, Title


class ListCreateDeleteViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                              mixins.DestroyModelMixin,
                              viewsets.GenericViewSet):
    pass


class GenreListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'


class CategoryListCreateDeleteViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer


def signup():
    pass


def get_token():
    pass
