from django.urls import path
from .views import AlbumRetriveView,PublicAlbumListView,AlbumCreateView,MyAlbumsListView,AlbumUpdateDeleteView,ArtistAlbumsListView

urlpatterns = [
    path('list/', PublicAlbumListView.as_view(), name='album-list'),  # list album for any user 
    path('my-albums/', MyAlbumsListView.as_view(), name='my-albums-list'),  # Changed from list-create
    path('create/', AlbumCreateView.as_view(), name='album-create'),  # list or create if artist
    path('retrieve/<int:pk>/', AlbumRetriveView.as_view(), name='album-retrieve'),  # retrieve an album for any user
    path('modify/<int:pk>/', AlbumUpdateDeleteView.as_view(), name='album-modify'),  # update, or delete an album
    path('artist/<int:artist_id>/', ArtistAlbumsListView.as_view(), name='artist-song-list'),  # list all Albums for a certain artist
    
]