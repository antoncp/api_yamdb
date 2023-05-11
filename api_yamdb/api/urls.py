from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryListCreateDeleteViewSet, CommentViewSet,
                       GenreListCreateDeleteViewSet, ReviewViewSet,
                       TitleViewSet)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreListCreateDeleteViewSet, basename='genres')
router_v1.register(
    'categories', CategoryListCreateDeleteViewSet, basename='categories'
)
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

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
