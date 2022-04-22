from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    def list(self, request, article_id):
        queryset = self.get_queryset()
        level = request.query_params.get('level')
        if level is not None:
            level = check_natural_number(level, 'level')
            queryset = queryset.filter(level__lte=int(level))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=['GET'],
        url_path=r'(?P<comment_id>\d+)/farther'
    )
    def get_farther_comment(self, request, article_id, comment_id):
        third_lvl_parent = get_object_or_404(
            self.get_queryset(),
            id=comment_id, level=3
        )
        queryset = self.get_queryset().filter(
            third_lvl_parent=third_lvl_parent
        )
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
