from django.urls import include, path
from rest_framework import routers

from api.views import ArticleViewSet

router = routers.DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')

urlpatterns = [
    path('', include(router.urls))
]
