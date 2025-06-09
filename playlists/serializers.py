from rest_framework import serializers
from .models import Playlist
from users.serializers import MiniUserSerializer
from songs.serializers import MiniSongSerializer
from songs.models import Song
from rest_framework.reverse import reverse

class PlaylistSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    songs = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        write_only=True,
        source='songs'  # Directly modifies the ManyToMany field
    )
    cover_art_url = serializers.SerializerMethodField() 

    class Meta:
        model = Playlist
        fields = [
            'id', 'name', 'owner', 'songs', 'song_ids', 
            'detail_url', 'created_at', 'cover_art','cover_art_url'
        ]
        read_only_fields = ['cover_art_url']
    
    def get_cover_art_url(self, obj):
        if obj.cover_art:
            return obj.cover_art.url
        return None
    
    def get_owner(self, obj):
        return MiniUserSerializer(obj.owner, context=self.context).data
    
    def get_songs(self, obj):
        return MiniSongSerializer(obj.songs.all(), many=True, context=self.context).data
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('playlist-retrieve', kwargs={'pk': obj.pk}))
        return None

    def create(self, validated_data):
        songs = validated_data.pop('songs', [])
        playlist = Playlist.objects.create(owner=self.context['request'].user, **validated_data)
        playlist.songs.set(songs)
        return playlist

    def update(self, instance, validated_data):
        # Remove songs from validated_data if present to prevent song modifications
        if 'songs' in validated_data:
            validated_data.pop('songs')
        
        # Update other fields only (name, cover_art, etc.)
        instance = super().update(instance, validated_data)
        return instance

class MiniPlaylistSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    detail_url = serializers.SerializerMethodField()
    cover_art_url = serializers.SerializerMethodField()    
    class Meta:
        model = Playlist
        fields = ['id', 'name', 'owner_name', 'cover_art', 'detail_url','cover_art_url']
        read_only_fields = ['cover_art_url']
        
    def get_cover_art_url(self, obj):
        if obj.cover_art:
            return obj.cover_art.url
        return None
    
    def get_detail_url(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request:
            return request.build_absolute_uri(reverse('playlist-retrieve', kwargs={'pk': obj.pk}))
        return None