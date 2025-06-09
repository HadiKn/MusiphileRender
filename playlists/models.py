from django.db import models
from django.contrib.auth import get_user_model
from songs.models import Song
from django.utils import timezone
from cloudinary.models import CloudinaryField
User = get_user_model()

class Playlist(models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(User,related_name="playlists",on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song,related_name="playlists",blank=True)
    created_at = models.DateField(auto_now_add=True)
    cover_art = CloudinaryField(
        'image',
        folder='playlists/covers/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

