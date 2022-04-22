from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

from api.models import Article, Comment
from api.serializers import ArticleSerializer, CommentSerializer
from api.validators import check_natural_number


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comment.objects.filter(article=article_id)

    def perform_create(self, serializer):
        article_id = self.kwargs.get('article_id')
        article = get_object_or_404(Article, id=article_id)
        serializer.save(article=article)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        level = request.query_params.get('level')
        if level is not None:
            level = check_natural_number(level, 'level')
            queryset = queryset.filter(level__lte=int(level))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
