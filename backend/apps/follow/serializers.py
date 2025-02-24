from .models import Follow
from rest_framework import serializers

from ..authors.serializers import AuthorSerializer


# kept type and summary here for the vibes, i think type will be used for inbox later on?
class FollowSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = ['type', 'summary', 'actor', 'object']

    def get_type(self, obj):
        return 'Follow'

    def get_summary(self, obj):
        return f"{obj.actor.displayName} -> {obj.object.displayName}"

class FollowingListSerializer(serializers.Serializer):
    type = serializers.CharField(default="following")
    following = AuthorSerializer(many=True)

class FollowersListSerializer(serializers.Serializer):
    type = serializers.CharField(default="followers")
    followers = AuthorSerializer(many=True)

class FriendsListSerializer(serializers.Serializer):
    type = serializers.CharField(default="friends")
    friends = AuthorSerializer(many=True)
