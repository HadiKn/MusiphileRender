from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
    regex=r'^[\w.@+ \-]+$',
    message='Username may contain letters, digits, spaces, and @/./+/-/_ characters.',
    code='invalid_username'
)]
    )
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='users/', blank=True, null=True)
    is_artist = models.BooleanField(default=False)

    def __str__(self):
        return self.username