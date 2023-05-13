from api.views import (CategoryListCreateDeleteViewSet, CommentViewSet,
                       GenreListCreateDeleteViewSet, ReviewViewSet,
                       TitleViewSet, UserViewSet, get_token, signup)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'titles', TitleViewSet, basename='titles'
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename='comments'
)
router_v1.register(r'users', UserViewSet)

category_list = CategoryListCreateDeleteViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
category_detail = CategoryListCreateDeleteViewSet.as_view({
    'delete': 'destroy',
})
genre_list = GenreListCreateDeleteViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
genre_detail = GenreListCreateDeleteViewSet.as_view({
    'delete': 'destroy',
})

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/categories/', category_list, name='category-list'),
    path(
        'v1/categories/<slug:slug>/', category_detail, name='category-detail',
    ),
    path('v1/genres/', category_list, name='genre-list'),
    path('v1/genres/<slug:slug>/', category_detail, name='genre-detail'),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]
