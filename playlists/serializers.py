from rest_framework import serializers
from .models import Playlist
from users.serializers import MiniUserSerializer
from songs.serializers import MiniSongSerializer
from songs.models import Song


class PlaylistSerializer(serializers.ModelSerializer):
    owner = MiniUserSerializer(read_only=True)
    songs = MiniSongSerializer(many=True, read_only=True)
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        write_only=True,
        source='songs'  # Directly modifies the ManyToMany field
    )

    def create(self, validated_data):
        songs = validated_data.pop('songs', [])
        playlist = Playlist.objects.create(**validated_data)
        playlist.songs.set(songs)
        return playlist

    def update(self, instance, validated_data):
        songs = validated_data.pop('songs', None)
        instance = super().update(instance, validated_data)
        if songs:
            instance.songs.add(*songs)  # This appends rather than replaces
        return instance

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'owner','songs','song_ids', 'created_at','cover_art']

class MiniPlaylistSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Playlist
        fields = ['id', 'name','owner_name','cover_art']