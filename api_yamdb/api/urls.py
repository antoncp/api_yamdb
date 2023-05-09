from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryListCreateDeleteViewSet,
                       GenreListCreateDeleteViewSet)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreListCreateDeleteViewSet, basename='genres')
router_v1.register(
    'categories', CategoryListCreateDeleteViewSet, basename='categories'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
