from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import uuid
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True,max_length=257)
    profile_picture = models.ImageField(upload_to="profile_pics/",blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class EmailConfimation(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return  str(self.token)