from rest_framework import serializers
from .models import Song
from albums.models import Album
from rest_framework.reverse import reverse

class SongSerializer(serializers.ModelSerializer):
    audio_file = serializers.FileField(required=False)
    audio_url = serializers.SerializerMethodField()
    artist = serializers.SerializerMethodField()
    album = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(),
        write_only=True,
        source='album', 
        required=False
    )

    class Meta:
        model = Song
        fields = [
            'id', 'title','play_count','artist', 'album', 'album_id', 'detail_url',
            'duration', 'audio_file', 'audio_url', 'cover_art', 
            'release_date', 'genre'
        ]
        read_only_fields = ['artist']
    
    def get_audio_url(self, obj):
        if obj.audio_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.audio_file.url)
            return obj.audio_file.url
        return None
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('song-retrieve', kwargs={'pk': obj.pk}))
        return None
    
    def validate_album_id(self, album):
        user = self.context['request'].user
        if album.artist != user:
            raise serializers.ValidationError(f"You cannot add your song to '{album.title}' because it does not belong to you.")
        return album

    def get_album(self, obj):
        from albums.serializers import MiniAlbumSerializer 
        if not obj.album:
            return None
        return MiniAlbumSerializer(
            obj.album,
            context=self.context  # This passes the request context to the nested serializer
        ).data
    
    def get_artist(self, obj):
        from users.serializers import MiniUserSerializer 
        return MiniUserSerializer(
            obj.artist,
            context=self.context  # This passes the request context to the nested serializer
        ).data

    def create(self, validated_data):
        album = validated_data.get('album')
        title = validated_data.get('title')
        artist = self.context['request'].user  # Get artist from request

        # Auto-create album if not provided
        if not album:
            album, _ = Album.objects.get_or_create(
                title=title, 
                artist=artist,
                defaults={'release_date': validated_data.get('release_date')}
            )
            validated_data['album'] = album

        # Check if a song with the same title and artist already exists
        if Song.objects.filter(title=title, artist=artist, album=album).exists():
            raise serializers.ValidationError(
                {'title': 'You already have a song with this title in the selected album.'}
            )
            
        # Set the artist from the request user
        validated_data['artist'] = artist
        
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
    detail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Song
        fields = ['id', 'title','play_count', 'artist_name', 'album_title', 'cover_art', 'detail_url']
    
    def get_detail_url(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request:
            return request.build_absolute_uri(reverse('song-retrieve', kwargs={'pk': obj.pk}))
        return None