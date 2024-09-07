# TODO: delete the unnecessary null = true from the field attribute
from django.db import models
from django.contrib.auth.models import User
import uuid
from user.models import Profile


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    name = models.CharField("Full Name", max_length=200)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    speciality = models.CharField("Speciality", max_length=200)
    phone_number = models.CharField("Phone Number", max_length=10)
    address = models.TextField("Address", default="default")
    experience = models.PositiveIntegerField("Year of Experience", default=0)
    about = models.TextField(blank=True)
    education = models.TextField(default="default_address")
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.speciality = self.speciality.capitalize()

        super().save(*args, **kwargs)

    # user the User class that have to username and the email field built in. this @property method help to access the user as it is part of the doctor table
    @property
    def username(self):
        return str(self.user.username)

    @property
    def email(self):
        return str(self.user.email)


class Opd(models.Model):
    owner = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name="opd")
    name = models.CharField("Name", max_length=255, null=True, blank=True)
    no_of_beds = models.PositiveIntegerField("No of Beds", default=0)
    no_of_appointment = models.PositiveIntegerField("No of Appointment", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)


class Inventory(models.Model):
    opd = models.OneToOneField(
        "Opd",
        on_delete=models.CASCADE,
        related_name="inventorys",
        null=True,
        blank=True,  # NOTE: initally after updating we are going to remove it
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Inventory of {str(self.opd.name)}"


class Medicine(models.Model):
    type = (("oral", "oral"), ("vascular", "vascular"), ("applicant", "applicant"))
    name = models.CharField("Name", max_length=255)
    category = models.CharField("Category", choices=type, max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        super().save(*args, **kwargs)


class Machinery(models.Model):
    name = models.CharField("Name", max_length=255)

    def __str__(self):
        return str(self.name)


class Inventory_Item(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="inventory_items"
    )
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="inventory_items",
        null=True,
        blank=True,
    )
    machinery = models.ForeignKey(
        Machinery,
        on_delete=models.CASCADE,
        related_name="inventory_items",
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField("Quantity", default=0)
    price = models.DecimalField("Price", max_digits=10, default=0, decimal_places=2)

    class Meta:
        verbose_name_plural = "Inventory Items"

    def __str__(self):
        return f"{self.medicine or self.machinery} in {self.inventory}"


class Offline_Patient(models.Model):
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    age = models.PositiveIntegerField("Age")
    email = models.EmailField("Email", max_length=190, null=True, blank=True)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    display_id = models.CharField("ID", max_length=30)
    phone_number = models.CharField("Phone Number", max_length=10)
    address = models.TextField("Address", default="default")
    medical_history = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)


class Appointment(models.Model):
    type = (
        ("online", "online"),
        ("offline", "offline"),
    )
    opd = models.ForeignKey(Opd, on_delete=models.CASCADE, related_name="appointments")
    offline_patient = models.ForeignKey(
        Offline_Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="offline_appoinments",
    )
    online_patient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="online_appointments",
    )

    appointment_type = models.CharField(
        "Appointment Type", choices=type, max_length=30, null=True
    )
    appointment_id = models.CharField("Appointment ID", max_length=10, null=True)
    date_of_appointment = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.appointment_id)

    class Meta:
        unique_together = [["opd", "appointment_id"]]

    def save(self, *args, **kwargs):
        # check if the appointment is new or not...
        is_new = self.id is None
        super().save(*args, **kwargs)

        if is_new:
            self.opd.no_of_appointment = models.F("no_of_appointment") + 1
            self.opd.save()

    def delete(self, *args, **kwargs):  # type: ignore
        self.opd.no_of_appointment = models.F("no_of_appointment") - 1
        self.opd.save()
        super().delete(*args, **kwargs)


class Patient(models.Model):
    type = (
        ("online", "online"),
        ("offline", "offline"),
    )
    opd = models.ForeignKey(Opd, on_delete=models.CASCADE, related_name="patients")
    offline_patient = models.ForeignKey(
        Offline_Patient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="offline_patients",
    )
    online_patient = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="online_patients",
    )

    patient_type = models.CharField(
        "Patient Type", choices=type, max_length=30, null=True
    )
    patient_id = models.CharField("Appointment ID", max_length=10, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [["opd", "patient_id"]]

    def __str__(self):
        return str(self.patient_id)

    def save(self, *args, **kwargs):
        # check if the appointment is new or not...
        is_new = self.id is None
        super().save(*args, **kwargs)

        if is_new:
            self.opd.no_of_beds = models.F("no_of_beds") + 1
            self.opd.save()

    def delete(self, *args, **kwargs):  # type: ignore
        self.opd.no_of_beds = models.F("no_of_beds") - 1
        self.opd.save()
        super().delete(*args, **kwargs)
