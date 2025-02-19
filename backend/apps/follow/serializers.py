from .models import Follow
from rest_framework import serializers

class FollowSerializer(serializers.ModelSerializer):
    type = 'follow'
    summary = serializers.CharField(max_length=255)

    class Meta:
        model = Follow
        fields = ['type', 'summary', 'actor', 'object']