from django.shortcuts import render
from .models import Playlist
from rest_framework import generics, permissions, filters
from .serializers import PlaylistSerializer, MiniPlaylistSerializer


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
