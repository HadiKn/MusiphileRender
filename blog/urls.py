from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostCreateView, 
    BlogPostRetrieveView,
    BlogPostUpdateDestroyView,
    ArtistBlogPostsListView,    
    MyBlogPostListView,
    CommentCreateView,
    CommentRetrieveUpdateDestroyView 
)

urlpatterns = [
    path('list/', BlogPostListView.as_view(), name='blogpost-list'),  # List all blog posts with search
    path('create/', BlogPostCreateView.as_view(), name='blogpost-create'),  #create or List your blog posts
    path('retrieve/<int:pk>/', BlogPostRetrieveView.as_view(), name='blogpost-retrieve'),  # Retrieve a blog post
    path('modify/<int:pk>/', BlogPostUpdateDestroyView.as_view(), name='blogpost-modify'),  # Update or delete a blog post
    path('artist/<int:artist_id>/', ArtistBlogPostsListView.as_view(), name='artist-blogpost-list'),  # List all blog posts by an artist
    path('my-posts/', MyBlogPostListView.as_view(), name='my-blogpost-list'),  # List all blog posts by the current user
    path('posts/<int:post_id>/comments/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),
]