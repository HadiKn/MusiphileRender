from django.db import models
from users.models import User
from songs.models import Song


class Stream(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='streams')
    song = models.ForeignKey(Song,on_delete=models.CASCADE,related_name='streams')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} streamed {self.song.title}"
    
    class Meta:
        ordering = ['-created_at']
 