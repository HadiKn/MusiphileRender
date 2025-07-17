from django.shortcuts import render
from .models import Playlist
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlaylistSerializer, MiniPlaylistSerializer
from songs.models import Song
from drf_spectacular.utils import extend_schema
from rest_framework import parsers

class PlaylistListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MiniPlaylistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']  
    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user) 



@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string', 'description': 'Name of the playlist'},
                'cover_art': {'type': 'string', 'format': 'binary', 'description': 'Optional cover art image'},
                'song_ids': {
                    'type': 'array',
                    'items': {'type': 'integer'},
                    'description': 'Optional list of song IDs to add to this playlist'
                }
            },
            'required': ['name']
        }
    }
)

class PlaylistCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlaylistSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']  
    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user) 

class PlaylistRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlaylistSerializer
    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)  


class AddSongsToPlaylistView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlaylistSerializer

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)
    
    def update(self, request, *args, **kwargs):
        playlist = self.get_object()
        
        # Get song IDs from request
        song_ids = request.data.get('song_ids', [])
        if not song_ids:
            return Response(
                {"error": "No song IDs provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the songs
        songs = Song.objects.filter(id__in=song_ids)
        if not songs.exists():
            return Response(
                {"error": "No valid songs found with the provided IDs"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Add songs to playlist
        playlist.songs.add(*songs)
        
        # Return updated playlist
        serializer = self.get_serializer(playlist)
        return Response(serializer.data)
