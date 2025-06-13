from django.shortcuts import render
from rest_framework import generics, permissions
from .models import BlogPost,Comment
from .serializers import BlogPostSerializer,MiniBlogPostSerializer,CommentSerializer
from users.permissions import IsArtist
from rest_framework import filters
from users.utils import api_response
from rest_framework import status


# list all posts for a certain artist
class ArtistBlogPostsListView(generics.ListAPIView):
    serializer_class = MiniBlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        artist_id = self.kwargs['artist_id']
        return BlogPost.objects.filter(author__id=artist_id)


# List all blog posts
class BlogPostListView(generics.ListAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = MiniBlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__username']

# Create a new blog post
class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated,IsArtist]

class MyBlogPostListView(generics.ListAPIView):
    serializer_class = MiniBlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)

# Retrieve a single blog post
class BlogPostRetrieveView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

# Update or Delete a blog post
class BlogPostUpdateDestroyView(generics.UpdateAPIView,generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated,IsArtist]
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return api_response(
            message="Blog post deleted successfully",
            status="success",
            status_code=status.HTTP_200_OK
        )

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        serializer.save(
            user=self.request.user,
            post_id=post_id
        )

class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return api_response(
            message="Comment deleted successfully",
            status="success",
            status_code=status.HTTP_200_OK
        )