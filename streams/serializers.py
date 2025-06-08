from rest_framework import serializers
from .models import Stream

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'user', 'song', 'created_at']
        read_only_fields = ['user', 'created_at']  # These will be set automatically