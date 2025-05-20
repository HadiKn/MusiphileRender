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
        # Since obj is a Follow object, we need to get all artists followed by the same follower
        follower = obj.follower
        # Find all artists this user follows
        artist_users = User.objects.filter(followers__follower=follower)
        return MiniUserSerializer(artist_users, many=True, context=self.context).data


class FollowerSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    
    class Meta:
        model = Follow
        fields = ['id', 'followers']
        
    def get_followers(self, obj):
        from users.serializers import MiniUserSerializer
        # Since obj is a Follow object, we need to get all followers of the same artist
        artist = obj.artist
        # Find all followers of this artist through the related_name
        follower_users = User.objects.filter(following__artist=artist)
        return MiniUserSerializer(follower_users, many=True, context=self.context).data