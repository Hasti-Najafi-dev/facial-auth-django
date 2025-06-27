from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)
    face_image_encode = models.JSONField(null=True, blank=True)  # If storing as a list

