from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Post, visibility_options, Comment, Like
from ..authors.models import Author
from ..authors.serializers import AuthorSerializer
from ..utils.paginators import LikesPaginator, CommentsPaginator

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
        request = self.context.get('request')
        queryset = Comment.objects.filter(post_id=obj.id)
        paginator = CommentsPaginator()
        paginated_comments = paginator.paginate_queryset(queryset, request)
        serializer = CommentSerializer(paginated_comments, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data


    def get_likes(self, obj):
        request = self.context.get('request')

        queryset = Like.objects.filter(object=obj.id_url)

        paginator = LikesPaginator()
        paginated_likes = paginator.paginate_queryset(queryset, request)

        serializer = LikeSerializer(paginated_likes, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

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

class CommentSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer(read_only=True)
    published = serializers.DateTimeField(read_only=True)
    comment = serializers.CharField(read_only=True)
    contentType = serializers.CharField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['type', 'author', 'comment', 'contentType', 'published', 'id', 'post', 'likes']

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "comment"

    def get_post(self, obj):
        return obj.post.id_url

    def get_likes(self, obj):
        #can pass context to serializer if needed for future permissions.
        request = self.context.get('request')
        queryset = Like.objects.filter(object=obj.id_url)

        paginator = LikesPaginator()
        paginated_likes = paginator.paginate_queryset(queryset, request)

        serializer = LikeSerializer(paginated_likes, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

class CommentCreateSerializer(serializers.ModelSerializer):
    # TODO: verify if it is going to be the ID or the entire post body object, then i gotta extract id out instead
    post = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ['comment', 'contentType', 'post']

    def create(self, validated_data):
        author_serial = self.context.get("view").kwargs.get("author_serial")
        author = get_object_or_404(Author, pk=author_serial)
        post_id = validated_data.pop('post')
        post = get_object_or_404(Post, id=post_id)

        comment = Comment.objects.create(
            author=author,
            post=post,
            **validated_data
        )
        comment.id_url = f"http://localhost:8000/api/authors/{author.id}/commented/{comment.id}"
        comment.save()
        return comment