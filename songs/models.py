from django.db import models
from albums.models import Album 
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField
User = get_user_model()

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, related_name='songs', on_delete=models.CASCADE)  # Linked to User (Artist)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE, blank=True, null=True)
    duration = models.DurationField(blank=True,null=True)  # The duration of the song
    audio_file = CloudinaryField(
        resource_type='video',  # This handles both audio and video files
        folder='songs/audio/',  # Optional: organize files in Cloudinary
        null=True,
        blank=True
    )
    cover_art = CloudinaryField(
        'image',
        folder='songs/covers/',
        null=True,
        blank=True
    )
    release_date = models.DateField(auto_now_add=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    play_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']