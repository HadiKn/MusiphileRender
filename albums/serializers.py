from rest_framework import serializers
from .models import Album
from django.contrib.auth import get_user_model
from users.serializers import MiniUserSerializer
from songs.serializers import MiniSongSerializer
from songs.models import Song
from rest_framework.reverse import reverse

User = get_user_model()

class AlbumSerializer(serializers.ModelSerializer):
    artist = MiniUserSerializer(read_only=True)
    songs = MiniSongSerializer(many=True, read_only=True)
    detail_url = serializers.SerializerMethodField()
    song_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Song.objects.all(),
        write_only=True,
        source='songs',
        required=False
    )
    cover_art_url = serializers.SerializerMethodField()


    class Meta:
        model = Album
        fields = [
            'id', 'title', 'artist', 'songs', 'song_ids', 
            'detail_url', 'release_date', 'cover_art','cover_art_url'
        ]
        read_only_fields = ['artist','cover_art_url']
    
    def get_cover_art_url(self, obj):
        if obj.cover_art:
            return obj.cover_art.url
        return "https://res.cloudinary.com/dswjejbhq/image/upload/v1756144236/file_00000000882461f981bc37afc2955813_y05i1l.png"

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(reverse('album-retrieve', kwargs={'pk': obj.pk}))
        return None

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
        
        if songs is not None:
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
    detail_url = serializers.SerializerMethodField()
    cover_art_url = serializers.SerializerMethodField()
    songs_count = serializers.IntegerField(source='songs.count', read_only=True) 

    
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist_name', 'cover_art', 'detail_url','cover_art_url','songs_count']
    
    def get_detail_url(self, obj):
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request:
            return request.build_absolute_uri(reverse('album-retrieve', kwargs={'pk': obj.pk}))
        return None
    
    def get_cover_art_url(self, obj):
        if obj.cover_art:
            return obj.cover_art.url
        return None