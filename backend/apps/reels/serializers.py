from rest_framework import serializers
from .models import Reel, ReelComment, ReelLike, ReelCommentLike
from ..authors.serializers import AuthorSerializer

class ReelCommentLikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    class Meta:
        model = ReelCommentLike
        fields = ['id', 'author', 'created_at']

class ReelCommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = ReelComment
        fields = ['id', 'content', 'contentType', 'author', 'created_at', 'likes_count', 'is_liked']
    
    def get_likes_count(self, obj):
        return obj.likes.count()
   
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                author = request.user.author_profile
                return obj.likes.filter(author=author).exists()
            except:
                return False
        return False

class ReelLikeSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    
    class Meta:
        model = ReelLike
        fields = ['id', 'author', 'created_at']

class ReelSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    video_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Reel
        fields = ['id', 'video', 'video_url', 'caption', 'author', 'created_at', 
                  'likes_count', 'comments_count', 'is_liked', 'view_count', 'duration',
                  'visibility']
        read_only_fields = ['id', 'created_at', 'view_count']
        
    def get_video_url(self, obj):
        """Return the absolute URL for the video."""
        if not obj.video:
            return None
            
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.video.url)
        return obj.video.url
        
    def create(self, validated_data):
        """Override to print debug information"""
        print("ReelSerializer.create() called with validated_data:", validated_data)
        return super().create(validated_data)
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                author = request.user.author_profile
                return obj.likes.filter(author=author).exists()
            except:
                return False
        return False