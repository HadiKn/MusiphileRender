from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Stream
from .serializers import StreamSerializer
from songs.models import Song
from users.utils import api_response

class StreamCreateView(generics.CreateAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        song_id = self.kwargs.get('song_id')
        song = get_object_or_404(Song, id=song_id)
        
        stream = Stream.objects.create(
            user=request.user,
            song=song
        )
        
        song.play_count = F('play_count') + 1
        song.save(update_fields=['play_count'])
        
        serializer = self.get_serializer(stream)
        return api_response(
            data=serializer.data,
            message="Stream recorded successfully",
            status_code=status.HTTP_201_CREATED
        )
