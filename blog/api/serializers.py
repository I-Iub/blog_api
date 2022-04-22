from django.shortcuts import get_object_or_404
from rest_framework import serializers

from api.models import Article, Comment
from api.validators import check_natural_number


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
            check_natural_number(parent_id, 'parent')
        return attrs

    def create(self, validated_data):
        parent_id = self.context.get('request').query_params.get('parent')
        # если параметр parent не передан, то это комментарий высшего уровня,
        # и у него нет предка-комментария - поле parent не заполняем
        if parent_id is None:
            return Comment.objects.create(level=1, **validated_data)

        parent = get_object_or_404(
            Comment,
            id=parent_id,
            article=validated_data.get('article')
        )
        # если родительский комментарий ниже третьего уровня вложенности,
        # то в поле third_lvl_parent ничего не записываем
        if parent.level < 3:
            instance = Comment.objects.create(
                level=parent.level + 1,
                parent=parent,
                **validated_data
            )
            return instance

        # если родительский комментарий - комментарий третьего уровня,
        # то в поле third_lvl_parent записываем его id
        if parent.level == 3:
            third_lvl_parent = parent
        # если у родительского комментария есть предок третьего уровня
        if parent.third_lvl_parent:
            third_lvl_parent = parent.third_lvl_parent

        instance = Comment.objects.create(
            third_lvl_parent=third_lvl_parent,
            level=parent.level + 1,
            parent=parent,
            **validated_data
        )
        return instance
