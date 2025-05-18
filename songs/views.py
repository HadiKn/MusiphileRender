from rest_framework import generics,permissions,filters
from .models import Song
from .serializers import SongSerializer,MiniSongSerializer
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsArtist



# list all songs for a certain artist
class ArtistSongsListView(generics.ListAPIView):
    serializer_class = MiniSongSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        artist_id = self.kwargs['artist_id']
        return Song.objects.filter(artist__id=artist_id)

# list or search for songs as a user
class PublicSongListView(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = MiniSongSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artist_name', 'album_title']

class SongRetrieveView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

# only for artists
class ArtistSongListCreateView(generics.ListCreateAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated,IsArtist]
    def get_queryset(self):
        return Song.objects.filter(artist=self.request.user)
    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)

class SongUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated,IsArtist]
    def get_queryset(self):
        return Song.objects.filter(artist=self.request.user)