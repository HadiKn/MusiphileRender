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
    artist_username = serializers.ReadOnlyField(source='artist.username')
    artist_profile_picture = serializers.ImageField(source='artist.profile_picture', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'artist', 'artist_username', 'artist_profile_picture']


class FollowerSerializer(serializers.ModelSerializer):
    follower_username = serializers.ReadOnlyField(source='follower.username')
    follower_profile_picture = serializers.ImageField(source='follower.profile_picture', read_only=True)
    
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_username', 'follower_profile_picture']