from django.urls import path
from .views import FollowCreateView, UnfollowView, UserFollowingListView, ArtistFollowersListView

urlpatterns = [
    path('follow/<int:artist_id>/', FollowCreateView.as_view(), name='follow-artist'), # follow artist
    path('unfollow/<int:artist_id>/', UnfollowView.as_view(), name='unfollow-artist'), # unfollow artist
    path('following/', UserFollowingListView.as_view(), name='user-following'), # show current user's follows
    path('following/<int:user_id>/', UserFollowingListView.as_view(), name='user-following-by-id'), # show specific user's follows
    path('followers/', ArtistFollowersListView.as_view(), name='artist-followers'),
    path('followers/<int:artist_id>/', ArtistFollowersListView.as_view(), name='artist-followers-by-id'), # show an artist followers
]
