from django.urls import path
from .views import PlaylistRetrieveView, PlaylistListView, PlaylistCreateView, AddSongsToPlaylistView

urlpatterns = [
    path('list/', PlaylistListView.as_view(), name='playlist-list'),  # list or create playlists
    path('create/', PlaylistCreateView.as_view(), name='playlist-create'),  # create a new playlist
    path('retrieve/<int:pk>/', PlaylistRetrieveView.as_view(), name='playlist-retrieve'),  # retrieve a playlist
    path('modify/<int:pk>/add-songs/', AddSongsToPlaylistView.as_view(), name='playlist-add-songs'),  # add songs to a playlist
]