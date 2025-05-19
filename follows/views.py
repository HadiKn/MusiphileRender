from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Follow
from .serializers import FollowSerializer, FollowingSerializer, FollowerSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowCreateView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        artist_id = self.kwargs.get('artist_id')
        try:
            artist = User.objects.get(id=artist_id)
        except User.DoesNotExist:
            raise ValidationError("Artist not found")
            
        # Check if the target user is an artist
        if not artist.is_artist:
            raise ValidationError("You can only follow users who are artists")
            
        # Check if user is trying to follow themselves
        if self.request.user == artist:
            raise ValidationError("You cannot follow yourself")
            
        # The unique_together constraint will handle duplicate follows
        serializer.save(follower=self.request.user, artist=artist)

class UnfollowView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        artist_id = self.kwargs.get('artist_id')
        try:
            return Follow.objects.get(
                follower=self.request.user,
                artist_id=artist_id
            )
        except Follow.DoesNotExist:
            raise ValidationError("You are not following this artist")

class UserFollowingListView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Only show the current user's follows
        return Follow.objects.filter(follower=self.request.user)

class ArtistFollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        artist_id = self.kwargs.get('artist_id')
        return Follow.objects.filter(artist_id=artist_id)