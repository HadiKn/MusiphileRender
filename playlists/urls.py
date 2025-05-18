from django.urls import path
from .views import PlaylistRetrieveView,PlaylistListView,PlaylistCreateView

urlpatterns = [
    path('list/', PlaylistListView.as_view(), name='playlist-list'),  # list or create playlists
    path('create/', PlaylistCreateView.as_view(), name='playlist-list'),  # list or create playlists
    path('retrieve/<int:pk>/', PlaylistRetrieveView.as_view(), name='playlist-modify'),  # retrieve, update, or delete a playlist
    
]