from rest_framework import generics,permissions,filters
from .models import Album
from .serializers import AlbumSerializer,MiniAlbumSerializer
from users.permissions import IsArtist


# list all Albums for a certain artist
class ArtistAlbumsListView(generics.ListAPIView):
    serializer_class = MiniAlbumSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        artist_id = self.kwargs['artist_id']
        return Album.objects.filter(artist__id=artist_id)

class AlbumRetriveView(generics.RetrieveAPIView):
    queryset = Album.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AlbumSerializer

class PublicAlbumListView(generics.ListAPIView):
    queryset = Album.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MiniAlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'artist__username']


class AlbumListCreateView(generics.ListCreateAPIView):
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated,IsArtist]
    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user)

class AlbumUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    serializer_class = AlbumSerializer
    ermission_classes = [permissions.IsAuthenticated,IsArtist]
    def get_queryset(self):
        return Album.objects.filter(artist=self.request.user)


