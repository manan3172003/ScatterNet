from copy import copy
from dodgerblue.settings import NODEHOSTNAME
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Post, visibility_options, Comment, Like
from ..authors.models import Author
from ..authors.serializers import AuthorSerializer, RemoteAuthorSerializer
from ..utils.paginators import LikesPaginator, CommentsPaginator

class PostSerializer(serializers.ModelSerializer):
    serial = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    page = serializers.URLField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    published = serializers.DateTimeField(read_only=True, default=None)

    class Meta:
        model = Post
        fields = ['serial', 'type', 'title', 'id', 'page', 'description', 'contentType', 'content', 'author', 'comments', 'likes', 'published', 'visibility']

    def create(self, validated_data):
        author_id = self.context['auth_id']
        author = Author.objects.get(id=author_id)
        post = Post.objects.create(author=author, **validated_data)

        # Update the post's id_url and page fields
        post.id_url = f"{NODEHOSTNAME}/api/authors/{author.id}/posts/{post.id}"
        post.page = f"{NODEHOSTNAME}/authors/{author.id}/posts/{post.id}"
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

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data

    def get_serial(self, obj):
        return obj.id

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "post"

    def get_comments(self, obj):
        request = self.context.get('request')
        queryset = Comment.objects.filter(post__id=obj.id)

        paginator = CommentsPaginator()
        request = copy(request)
        request.query_params._mutable = True
        request.query_params[paginator.page_size_query_param] = '5'
        request.query_params['page'] = '1'

        paginated_comments = paginator.paginate_queryset(queryset, request)

        serializer = CommentSerializer(paginated_comments, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data


    def get_likes(self, obj):
        #can pass context to serializer if needed for future permissions.
        request = self.context.get('request')
        queryset = Like.objects.filter(object=obj.id_url)

        request = copy(request)
        request.query_params._mutable = True
        paginator = LikesPaginator()
        request.query_params[paginator.page_size_query_param] = '5'
        request.query_params['page'] = '1'

        paginated_likes = paginator.paginate_queryset(queryset, request)

        serializer = LikeSerializer(paginated_likes, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data


class LikeSerializer(serializers.ModelSerializer):
    serial = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    published = serializers.DateTimeField(read_only=True)
    object = serializers.URLField(read_only=True)

    class Meta:
        model = Like
        fields = ['serial', 'type', 'author', 'published', 'id', 'object']

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "like"

    def get_serial(self, obj):
        return obj.id

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data

class CommentSerializer(serializers.ModelSerializer):
    serial = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    published = serializers.DateTimeField(read_only=True)
    comment = serializers.CharField(read_only=True)
    contentType = serializers.CharField(read_only=True)
    post = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = ['serial', 'type', 'author', 'comment', 'contentType', 'published', 'id', 'post', 'likes']

    def get_id(self, obj):
        return obj.id_url

    def get_type(self, obj):
        return "comment"

    def get_post(self, obj):
        return obj.post.id_url

    def get_serial(self, obj):
        return obj.id

    def get_author(self, obj):
        return AuthorSerializer(obj.author).data

    def get_likes(self, obj):
        #can pass context to serializer if needed for future permissions.
        request = self.context.get('request')
        queryset = Like.objects.filter(object=obj.id_url)

        request = copy(request)
        request.query_params._mutable = True
        paginator = LikesPaginator()
        request.query_params[paginator.page_size_query_param] = '5'
        request.query_params['page'] = '1'

        paginated_likes = paginator.paginate_queryset(queryset, request)

        serializer = LikeSerializer(paginated_likes, many=True, context=self.context)
        return paginator.get_paginated_response(serializer.data).data

class CommentCreateSerializer(serializers.ModelSerializer):
    post = serializers.URLField(write_only=True)

    class Meta:
        model = Comment
        fields = ['comment', 'contentType', 'post']

    def create(self, validated_data):
        author_serial = self.context.get("view").kwargs.get("author_serial")
        author = get_object_or_404(Author, pk=author_serial)
        post_id_url = validated_data.pop('post')
        post = get_object_or_404(Post, id_url=post_id_url)

        comment = Comment.objects.create(
            author=author,
            post=post,
            **validated_data
        )
        comment.id_url = f"{NODEHOSTNAME}/api/authors/{author.id}/commented/{comment.id}"
        comment.save()
        return comment

class RemotePostSerializer(serializers.ModelSerializer):
    serial = serializers.SerializerMethodField(read_only=True)
    id = serializers.URLField()
    page = serializers.URLField()
    type = serializers.SerializerMethodField(read_only=True)
    author = AuthorSerializer()
    comments = CommentSerializer(many=True)
    likes = LikeSerializer(many=True)
    published = serializers.DateTimeField()
    class Meta:
        model = Post
        fields = ['serial', 'type', 'title', 'id', 'page', 'description', 'contentType', 'content', 'author', 'comments', 'likes', 'published', 'visibility']

class RemoteLikeSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    serial = serializers.SerializerMethodField(read_only=True)
    id = serializers.URLField()
    author = RemoteAuthorSerializer()

    class Meta:
        model = Like
        fields = ('serial', 'type', 'id', 'author', 'published', 'object')

    def create(self, validated_data):
        authorserializer = RemoteAuthorSerializer(data=validated_data.get('author'))
        authorserializer.is_valid(raise_exception=True)
        try:
            author = Author.objects.get(id_url=validated_data.get('author').get('id'))
        except Author.DoesNotExist:
            author = authorserializer.save()

        validated_data.pop('author')

        like = Like.objects.create(
            author=author,
            id_url=validated_data.get('id'),
            published=validated_data.get('published'),
            object=validated_data.get('object')
        )
        like.save()
        return like

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['id'] = instance.id_url
        return data

    def get_type(self, obj):
        return "like"

    def get_serial(self, obj):
        return obj.id