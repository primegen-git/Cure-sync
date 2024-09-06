from django.db import models
from django.contrib.auth.models import User
import uuid
from user.models import Profile


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    username = models.CharField("Username", max_length=200)
    name = models.CharField("Full Name", max_length=200)
    email = models.EmailField("Email", max_length=190)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    speciality = models.CharField("Speciality", max_length=200)
    phone_number = models.CharField("Phone Number", max_length=10)
    address = models.TextField("Address", default="default")
    experience = models.IntegerField("Year of Experience", default=0)
    about = models.TextField(blank=True)
    education = models.TextField(default="default_address")
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.name = self.name.upper()
        self.speciality = self.speciality.capitalize()

        super().save(*args, **kwargs)


class Offline_Patient(models.Model):
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    age = models.IntegerField("Age")
    display_id = models.CharField("ID", max_length=30)
    phone_number = models.CharField("Phone Number", max_length=10)
    address = models.TextField("Address", default="default")
    medical_history = models.TextField()
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


class Medicine(models.Model):
    type = (("oral", "oral"), ("vascular", "vascular"), ("applicant", "applicant"))
    name = models.CharField("Name", max_length=255)
    category = models.CharField("Category", choices=type, max_length=30)
    price = models.IntegerField("Price", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class Inventory(models.Model):
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="inventory"
    )
    quantity = models.IntegerField("Quantity", default=0)
    machinary = models.CharField("Machinary", max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )


class Opd(models.Model):
    owner = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name="opd")
    name = models.CharField("Name", max_length=255)
    no_of_beds = models.IntegerField("No of Beds", default=0)
    no_of_appointment = models.IntegerField("No of Appointment", default=0)
    online_patient = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="online_patient"
    )
    offline_patients = models.ManyToManyField(Offline_Patient, related_name="opds")
    inventory = models.OneToOneField(
        Inventory, on_delete=models.CASCADE, related_name="opd"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)
