import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """
    Filter Title queryset by category slug,
    genre slug, year and/or name fields.

    """
    category = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='iexact'
    )
    genre = django_filters.CharFilter(
        field_name='genre__slug', lookup_expr='iexact'
    )
    year = django_filters.NumberFilter(
        field_name='year', lookup_expr='exact'
    )
    name = django_filters.CharFilter(
        field_name='name', lookup_expr='iexact'
    )

    class Meta:
        model = Title
        fields = ('category', 'genre', 'year', 'name')
