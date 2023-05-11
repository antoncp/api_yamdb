from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import (CategoryListCreateDeleteViewSet,
                       GenreListCreateDeleteViewSet,
                       TitleViewSet, signup, get_token)


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('genres', GenreListCreateDeleteViewSet, basename='genres')
router_v1.register(
    'categories', CategoryListCreateDeleteViewSet, basename='categories'
)
router_v1.register(
    'titles', TitleViewSet, basename='titles'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]
