from django.utils import timezone
from rest_framework import serializers
from .models import Post, visibility_options, Comment, Like
from ..authors.models import Author
from ..authors.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)
    page = serializers.URLField(read_only=True)
    type = serializers.CharField(read_only=True, default='post')
    author = AuthorSerializer(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    published = serializers.DateTimeField(read_only=True, default=None)

    class Meta:
        model = Post
        fields = ['type', 'title', 'id', 'page', 'description', 'contentType', 'content', 'author', 'comments', 'likes', 'published', 'visibility']

    def create(self, validated_data):
        author_id = self.context['auth_id']
        author = Author.objects.get(id=author_id)
        post = Post.objects.create(author=author, **validated_data)

        # Update the post's id_url and page fields
        post.id_url = f"http://localhost:8000/api/posts/{post.id}"
        post.page = f"http://localhost:8000/posts/{post.id}"
        post.save()
        return post

    def update(self, instance, validated_data):
        # Update only specific fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.content = validated_data.get('content', instance.content)
        instance.visibility = validated_data.get('visibility', instance.visibility)

        # Automatically update the published date
        instance.published = timezone.now()

        instance.save()
        return instance

    def get_id(self, obj):
        return obj.id_url

    def get_comments(self, obj):
        return {}

    def get_likes(self, obj):
        return {}

class LikeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer(read_only=True)
    published = serializers.DateTimeField(read_only=True)
    object = serializers.URLField(read_only=True)

    class Meta:
        model = Like
        fields = ['type', 'author', 'published', 'id', 'object']

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "like"


