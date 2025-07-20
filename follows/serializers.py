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
    artists = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'artists']
    def get_artists(self, obj):
        from users.serializers import MiniUserSerializer
        follower = obj.follower
        artist_users = User.objects.filter(followers__follower=follower)
        return MiniUserSerializer(artist_users, many=True, context=self.context).data


class FollowerSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'followers']
        
    def get_followers(self, obj):
        from users.serializers import MiniUserSerializer
        artist = obj.artist
        follower_users = User.objects.filter(following__artist=artist)
        return MiniUserSerializer(follower_users, many=True, context=self.context).data