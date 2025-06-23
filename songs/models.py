from django.db import models
from albums.models import Album 
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField
import os
from datetime import timedelta
import mutagen
from django.core.exceptions import ValidationError

User = get_user_model()

class Song(models.Model):
    # Supported audio formats
    SUPPORTED_FORMATS = [
        '.mp3',
        '.wav',
        '.ogg',
        '.m4a',
        '.flac',
        '.aac',
    ]
    
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

    def clean(self):
        super().clean()
        if self.audio_file:
            # Get file extension
            _, ext = os.path.splitext(self.audio_file.name.lower())
            if ext not in self.SUPPORTED_FORMATS:
                raise ValidationError(
                    f'Unsupported file format. Supported formats: { ", ".join(self.SUPPORTED_FORMATS) }'
                )

    class Meta:
        ordering = ['-release_date']