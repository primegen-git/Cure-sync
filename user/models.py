import uuid

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    BLOOD_TYPE = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    gender_type = [
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    gender = models.CharField("Gender", max_length=10, choices=gender_type, null=True)
    age = models.PositiveIntegerField("Age", null=True)
    date_of_birth = models.DateField("Date of Birth", null=True)
    blood_group = models.CharField(
        "Blood Type", max_length=6, choices=BLOOD_TYPE, null=True
    )
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.jpg",
    )
    phone_number = models.CharField("Phone Number", max_length=10, null=True)
    address = models.TextField("Address", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    def get_opd(self):
        if hasattr(self, "online_appointment") and self.online_appointment:  # type: ignore
            return self.online_appointment.opd  # type: ignore
        return None

    def get_appointment(self):
        if hasattr(self, "online_appointment") and self.online_appointment:  # type: ignore
            return self.online_appointment  # type: ignore
        return None
