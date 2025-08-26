from rest_framework import serializers
from .models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'artist', 'follower']
        read_only_fields = ['follower','artist']


class FollowingSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'artist']
    
    def get_artist(self, obj):
        from users.serializers import MiniUserSerializer
        return MiniUserSerializer(obj.artist, context=self.context).data

class FollowerSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'follower']
    
    def get_follower(self, obj):
        from users.serializers import MiniUserSerializer
        return MiniUserSerializer(obj.follower, context=self.context).data