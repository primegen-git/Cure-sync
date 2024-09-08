from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    gender_type = (
        ("male", "male"),
        ("female", "female"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    age = models.PositiveIntegerField("Age", null=True)
    gender = models.CharField("Gender", max_length=10, choices=gender_type, null=True)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    phone_number = models.CharField("Phone Number", max_length=10, null=True)
    address = models.TextField("Address", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email
