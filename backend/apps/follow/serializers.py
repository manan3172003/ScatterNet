from .models import Follow
from rest_framework import serializers

from ..authors.serializers import AuthorSerializer, RemoteAuthorSerializer
from ..authors.models import Author


# kept type and summary here for the vibes, i think type will be used for inbox later on?
class FollowSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    summary = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = ['type', 'summary', 'actor', 'object']

    def get_type(self, obj):
        return 'follow'

    def get_summary(self, obj):
        return f"{obj.actor.displayName} -> {obj.object.displayName}"

class RemoteFollowSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField(read_only=True)
    summary = serializers.SerializerMethodField(read_only=True)
    actor = RemoteAuthorSerializer()
    object = RemoteAuthorSerializer()

    class Meta:
        model = Follow
        fields = ['type', 'summary', 'actor', 'object']

    def create(self, validated_data):
        try:
            actor_author = Author.objects.get(id_url=validated_data.get('actor').get('id'))
        except Author.DoesNotExist:
            actor_author = RemoteAuthorSerializer(data=validated_data.get('actor'))
            actor_author.is_valid(raise_exception=True)
            actor_author = actor_author.save()

        try:
            object_author = Author.objects.get(id_url=validated_data.get('object').get('id'))
        except Author.DoesNotExist:
            object_author = RemoteAuthorSerializer(data=validated_data.get('object'))
            object_author.is_valid(raise_exception=True)
            object_author = object_author.save()

        follow = Follow.objects.create(
            actor=actor_author,
            object=object_author
        )

        return follow

    def get_type(self, obj):
        return 'follow'

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
