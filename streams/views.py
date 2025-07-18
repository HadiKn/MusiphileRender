from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Stream
from .serializers import StreamSerializer, StreamHistorySerializer
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

class UserStreamHistoryView(generics.ListAPIView):
    """
    API endpoint that allows users to view their stream history.
    Returns songs in the same format as the songs/list/ endpoint.
    """
    serializer_class = StreamHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['-created_at']  # Default: newest first
    ordering = ['-created_at']
    pagination_class = None  # This disables pagination

    def get_queryset(self):
        """
        Return the stream history for the currently authenticated user.
        """
        return Stream.objects.filter(user=self.request.user).select_related('song', 'song__artist', 'song__album')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return api_response(
            data=serializer.data,
            message="Stream history retrieved successfully",
            status_code=status.HTTP_200_OK
        )
