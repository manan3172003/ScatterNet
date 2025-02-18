from rest_framework import serializers
from .models import Post, visibility_options


class PostSerializer(serializers.Serializer):
    type = 'post'
    title = serializers.CharField(max_length=200)
    id_url = None
    page = serializers.URLField()
    description = serializers.CharField(max_length=200)
    contentType = serializers.CharField(max_length=100)
    content = serializers.CharField()
    # need to change when author serializer is made
    author_id = serializers.CharField(required=True)
    published = None
    visibility = serializers.ChoiceField(choices=visibility_options, default='PUBLIC')


    def create(self, validated_data):
        # creates the object
        post = Post.objects.create(**validated_data)
        # updates the url_id to the actual value
        post.id_url = "http://localhost:8000/api/posts/{}".format(post.id)
        post.page = "http://localhost:8000/posts/{}".format(post.id)
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.content = validated_data.get('content', instance.content)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.save()
        return instance