from rest_framework import serializers

from news.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'body', 'is_active', 'created_at',  'updated_at')

        extra_kwargs = {
            'is_active': {'read_only': True},
            'user': {'read_only': True},
            'post': {'read_only': True}
        }

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.body = validated_data['body']
        instance.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    post_comment_count = serializers.SerializerMethodField('get_post_comment_count')

    class Meta:
        model = Post
        fields = ('id', 'user', 'title', 'slug', 'body', 'image', 'category',
                  'status', 'tags', 'view_count', 'post_comment_count', 'publish_time', 'created_at', 'updated_at')

        extra_kwargs = {
            'view_count': {'read_only': True},
            'user': {'read_only': True}
        }

    def get_post_comment_count(self, obj):
        return obj.comments.count()

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', None)

        post = Post.objects.create(**validated_data)

        if tags_data:
            post.tags.set(tags_data)

        return post
