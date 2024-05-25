from rest_framework import generics
from rest_framework import permissions

from common.custom_permissions import IsAuthor
from news.models import Post, Comment
from news import serializers


class PostsListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.AllowAny,)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAdminUser, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (IsAuthor, )
    lookup_field = 'slug'


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (IsAuthor, )
    lookup_field = 'slug'


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.AllowAny, )
    lookup_field = 'slug'


class PostsDraftAPIView(generics.ListAPIView):
    queryset = Post.objects.filter(status=Post.Status.draft)
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAdminUser,)


class PostCategoryAPIView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        category = self.kwargs['category']
        return Post.objects.filter(category__title=category)


class PostTagAPIView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        tag = self.kwargs['tag']
        return Post.objects.filter(tags__title=tag)


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAdminUser,)


class PostCommentListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs['slug']
        post = Post.objects.get(slug=slug)
        return post.comments.all()

    def perform_create(self, serializer):
        slug = self.kwargs['slug']
        post = Post.objects.get(slug=slug)
        serializer.save(user=self.request.user, post=post)


class PostCommentUpdateAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthor,)
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Comment.objects.filter(id=pk)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
