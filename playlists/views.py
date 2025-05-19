from django.shortcuts import render
from .models import Playlist
from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PlaylistSerializer, MiniPlaylistSerializer
from songs.models import Song


class PlaylistListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MiniPlaylistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']  
    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user) 

class PlaylistCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PlaylistSerializer
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
