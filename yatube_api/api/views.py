from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

from .models import Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


# from rest_framework.viewsets import GenericViewSet
# from rest_framework.mixins import CreateModelMixin, ListModelMixin

# class MethodViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
#     pass
#
# @permission_classes([IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly])
# class GroupViewSet(MethodViewSet):
#     ...
#
# @permission_classes([IsAuthenticated])
# class FollowViewSet(MethodViewSet):
#     ...


@permission_classes([IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly])
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@permission_classes([IsAuthorOrReadOnly, IsAuthenticated])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['id'])
        serializer.save(post=post, author=self.request.user)


@permission_classes([IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly])
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post']


@permission_classes([IsAuthenticated])
class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'following__username']
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return self.request.user.following.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
