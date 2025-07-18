from rest_framework import serializers
from .models import Stream
from songs.serializers import MiniSongSerializer

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'user', 'song', 'created_at']
        read_only_fields = ['user', 'created_at']

class StreamHistorySerializer(serializers.ModelSerializer):
    song = MiniSongSerializer()

    class Meta:
        model = Stream
        fields = [
            'song', 'created_at'
        ]