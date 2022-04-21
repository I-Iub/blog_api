from django.urls import include, path
from rest_framework import routers

from api.views import ArticleViewSet, CommentViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('articles', ArticleViewSet, basename='articles')
router_v1.register(
    r'articles/(?P<article_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
