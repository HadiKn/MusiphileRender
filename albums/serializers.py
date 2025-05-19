from rest_framework import serializers
from .models import Album
from django.contrib.auth import get_user_model
from users.serializers import MiniUserSerializer
from songs.serializers import MiniSongSerializer
from songs.models import Song

User = get_user_model()


class AlbumSerializer(serializers.ModelSerializer):
    artist = MiniUserSerializer(read_only=True)
    songs = MiniSongSerializer(many=True,read_only=True)
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        write_only=True,
        source='songs',
        required=False
    )

    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'songs', 'song_ids', 'release_date', 'cover_art']
        read_only_fields = ['artist']

    def validate_song_ids(self, songs):
        user = self.context['request'].user
        for song in songs:
            if song.artist != user:
                raise serializers.ValidationError(f"You cannot add the song '{song.title}' because it does not belong to you.")
        return songs

    def create(self, validated_data):
        songs = validated_data.pop('songs', [])
        album = Album.objects.create(artist=self.context['request'].user, **validated_data)
        album.songs.set(songs)
        return album
    
    def update(self, instance, validated_data):
        songs = validated_data.pop('songs', None)
        instance = super().update(instance, validated_data)
        
        if songs:
            # Store old albums before updating song relationships
            old_albums = {}
            for song in songs:
                if song.album and song.album != instance:
                    old_albums[song.album.id] = song.album
            
            # Update song relationships
            for song in songs:
                song.album = instance
                song.save()
            
            # Check if any old albums are now empty and delete them
            for album_id, album in old_albums.items():
                if album.songs.count() == 0:
                    album.delete()
                    
        return instance


class MiniAlbumSerializer(serializers.ModelSerializer):
    artist_name = serializers.ReadOnlyField(source='artist.username')
    class Meta:
        model = Album
        fields = ['id', 'title','artist_name','cover_art']