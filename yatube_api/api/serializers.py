from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import (Post,
                          Group,
                          Comment,
                          )


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели постов."""
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('group', 'pub_date',)


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор модели групп."""
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор модели комментариев."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
