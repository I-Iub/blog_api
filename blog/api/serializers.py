from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'text')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'level', 'parent', 'text']
        read_only_fields = ['article', 'level', 'parent']

    def validate(self, attrs):
        parent_id = self.context.get('request').query_params.get('parent')
        if parent_id is not None:
            try:
                parent_id = int(parent_id)
                if parent_id < 1:
                    raise serializers.ValidationError(
                        {"parent": "Число должно быть больше нуля"}
                    )
            except ValueError:
                raise serializers.ValidationError(
                    {"parent": "Число должно быть натуральным"}
                )
        return attrs

    def create(self, validated_data):
        parent_id = self.context.get('request').query_params.get('parent')
        if parent_id is None:
            return Comment.objects.create(level=1, **validated_data)

        parent = get_object_or_404(
            Comment,
            id=parent_id,
            article=validated_data.get('article')
        )
        instance = Comment.objects.create(
            level=parent.level + 1,
            parent=parent,
            **validated_data
        )
        return instance
