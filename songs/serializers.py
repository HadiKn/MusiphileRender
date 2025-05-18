from rest_framework import serializers
from .models import Song
from albums.models import Album

class SongSerializer(serializers.ModelSerializer):
    audio_file = serializers.FileField(required=False)
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        write_only=True,
        source='album', 
        required=False
    )

    class Meta:
        model = Song
        fields = [
            'id', 'title', 'artist', 'album', 'album_id',
            'duration', 'audio_file', 'cover_art',
            'release_date', 'genre'
        ]
        read_only_fields = ['artist']

    def get_album(self, obj):
        from albums.serializers import MiniAlbumSerializer 
        return MiniAlbumSerializer(obj.album).data
    def get_artist(self, obj):
        from users.serializers import MiniUserSerializer 
        return MiniUserSerializer(obj.artist).data

    def create(self, validated_data):
        album = validated_data.get('album')
        title = validated_data.get('title')
        artist = self.context['request'].user  # Get artist from request

        # Create album automatically if not provided
        if not album:
            album, _ = Album.objects.get_or_create(title=title, artist=artist)
            validated_data['album'] = album

        validated_data['artist'] = artist  # Explicitly assign artist
        return super().create(validated_data)
    def update(self, instance, validated_data):
        old_album = instance.album
        response = super().update(instance, validated_data)
        new_album = instance.album  # Updated album after save

        # Delete old album if it's now empty
        if old_album != new_album and old_album.songs.count() == 0:
            old_album.delete()

        return response



class MiniSongSerializer(serializers.ModelSerializer):
    artist_name = serializers.ReadOnlyField(source='artist.username')
    album_title = serializers.ReadOnlyField(source='album.title')

    class Meta:
        model = Song
        fields = ['id', 'title','artist_name','album_title','cover_art']