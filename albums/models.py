from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cloudinary.models import CloudinaryField

User = get_user_model()

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(User, related_name='albums', on_delete=models.CASCADE)
    release_date = models.DateField(auto_now_add=True)
    cover_art = CloudinaryField(
        'image',
        folder='albums/covers/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title