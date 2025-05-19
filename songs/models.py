from django.db import models
from albums.models import Album 
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, related_name='songs', on_delete=models.CASCADE)  # Linked to User (Artist)
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE, blank=True, null=True)
    duration = models.DurationField(blank=True)  # The duration of the song
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)  # Link to the song's audio file
    cover_art = models.ImageField(upload_to='song_covers/', blank=True, null=True)
    release_date = models.DateField(default=timezone.now().date())
    genre = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-release_date']