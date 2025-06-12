from django.urls import path
from .views import PublicSongListView,ArtistSongListCreateView,SongRetrieveView,SongUpdateDeleteView,ArtistSongsListView

urlpatterns = [
    path('list/', PublicSongListView.as_view(), name='song-list'),  # list songs for any user 
    path('list-create/', ArtistSongListCreateView.as_view(), name='song-create'),  # list or create if artist
    path('retrieve/<int:pk>/', SongRetrieveView.as_view(), name='song-retrieve'),  # retrieve a song for any user
    path('modify/<int:pk>/', SongUpdateDeleteView.as_view(), name='song-modify'),  # update, or delete a song
    path('artist/<int:artist_id>/', ArtistSongsListView.as_view(), name='artist-song-list'),  # list all songs for a certain artist
]