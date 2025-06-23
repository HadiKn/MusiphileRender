from rest_framework import generics,permissions,filters,parsers
from .models import Song
from .serializers import SongSerializer,MiniSongSerializer
from rest_framework.exceptions import PermissionDenied
from users.permissions import IsArtist
from drf_spectacular.utils import extend_schema


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
    search_fields = ['title', 'artist__username', 'album__title']

class SongRetrieveView(generics.RetrieveAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated]

# only for artists
# For listing artist's songs (using MiniSongSerializer)
class MySongsListView(generics.ListAPIView):
    serializer_class = MiniSongSerializer
    permission_classes = [permissions.IsAuthenticated, IsArtist]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'album__title']
    def get_queryset(self):
        return Song.objects.filter(artist=self.request.user)

# For creating a new song (using SongSerializer)

@extend_schema(
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'album_id': {'type': 'integer', 'description': 'Optional ID of an existing album'},
                'duration': {'type': 'string', 'format': 'time', 'description': 'Duration in HH:MM:SS format'},
                'audio_file': {'type': 'string', 'format': 'binary', 'description': 'Audio file to upload'},
                'cover_art': {'type': 'string', 'format': 'binary', 'description': 'Optional cover art image'},
                'genre': {'type': 'string', 'description': 'Optional genre of the song'},
                'release_date': {'type': 'string', 'format': 'date', 'description': 'Optional release date (YYYY-MM-DD)'}
            },
            'required': ['title']
        }
    }
)
class SongCreateView(generics.CreateAPIView):
    serializer_class = SongSerializer
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]
    permission_classes = [permissions.IsAuthenticated, IsArtist]
    
    def perform_create(self, serializer):
        serializer.save(artist=self.request.user)

class SongUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = SongSerializer
    permission_classes = [permissions.IsAuthenticated,IsArtist]
    def get_queryset(self):
        return Song.objects.filter(artist=self.request.user)