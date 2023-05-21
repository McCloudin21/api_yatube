from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.permissions import AuthorOrReadOnlyPermissions
from api.serializers import (CommentSerializer,
                             GroupSerializer,
                             PostSerializer,
                             )
from posts.models import (Post,
                          Group,
                          )


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, записи и изменения постов."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,
                          AuthorOrReadOnlyPermissions,
                          )

    def perform_create(self, serializer):
        """Метод создания нового поста."""
        return serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет получения данных групп пользователей."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет получения, записи и изменения комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,
                          AuthorOrReadOnlyPermissions,
                          )

    def get_queryset(self):
        """Метод выбора всех комментариев по нужному посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        return post.comments

    def perform_create(self, serializer):
        """Метод создания нового комментария по нужному посту."""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)
