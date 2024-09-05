from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = models.CharField("Username", max_length=200, null=True, blank=True)
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    email = models.EmailField("Email", max_length=190, null=True, blank=True)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.name = self.name.upper()

        super().save(*args, **kwargs)
