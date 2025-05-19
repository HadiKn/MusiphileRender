from enum import unique
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Follow(models.Model):
    follower = models.ForeignKey(User,related_name="following",on_delete=models.CASCADE)
    artist = models.ForeignKey(User,related_name="followers",on_delete=models.CASCADE)
    class Meta:
        unique_together = ('follower', 'artist')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.artist.username}"
