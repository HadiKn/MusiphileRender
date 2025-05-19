from django.urls import path
from .views import FollowCreateView, UnfollowView, UserFollowingListView, ArtistFollowersListView

urlpatterns = [
    path('follow/<int:artist_id>/', FollowCreateView.as_view(), name='follow-artist'), # follow artist
    path('unfollow/<int:artist_id>/', UnfollowView.as_view(), name='unfollow-artist'), # unfollow artist
    
    path('following/', UserFollowingListView.as_view(), name='user-following'), # show who you are following
    path('followers/<int:artist_id>/', ArtistFollowersListView.as_view(), name='artist-followers'), # show an artist followers
]
