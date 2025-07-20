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
    
    def create(self, request, *args, **kwargs):
        artist_id = self.kwargs.get('artist_id')
        try:
            artist = User.objects.get(id=artist_id)
            
            # Check if the target user is an artist
            if not artist.is_artist:
                return Response(
                    {"error": "You can only follow users who are artists"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Check if user is trying to follow themselves
            if self.request.user == artist:
                return Response(
                    {"error": "You cannot follow yourself"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            # Check if already following
            if Follow.objects.filter(follower=self.request.user, artist=artist).exists():
                return Response(
                    {"error": "You are already following this artist"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            follow = Follow.objects.create(follower=self.request.user, artist=artist)
            serializer = self.get_serializer(follow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except User.DoesNotExist:
            return Response(
                {"error": "Artist not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class UnfollowView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowSerializer
    
    def get_object(self):
        artist_id = self.kwargs.get('artist_id')
        try:
            return Follow.objects.get(
                follower=self.request.user,
                artist_id=artist_id
            )
        except Follow.DoesNotExist:
            raise ValidationError({"error": "You are not following this artist"})
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Successfully unfollowed"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

class UserFollowingListView(generics.ListAPIView):
    serializer_class = FollowingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        if user_id:
            # Show follows for the specified user
            return Follow.objects.filter(follower_id=user_id)
        else:
            # Show follows for the current authenticated user
            return Follow.objects.filter(follower=self.request.user)

class ArtistFollowersListView(generics.ListAPIView):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        artist_id = self.kwargs.get('artist_id')
        if artist_id :
            return Follow.objects.filter(artist_id=artist_id)
        else:
            return Follow.objects.filter(artist=self.request.user)