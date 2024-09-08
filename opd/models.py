# TODO: change the "date_of_appointment" -> date
# TODO: delete the unnecessary null = true from the field attribute
# TODO: create a single table  replacing the medicine table with four catogery (existing + machinary)
# TODO: add a new attribute in the appointment table which check if the online_patient appointment request is approved or not
from django.db import models, transaction
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
        return self.user.username

    @property
    def email(self):
        return self.user.email


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
        return f"Opd of {self.owner.name}"

    @property
    def patient_count(self):
        if self.patients.count() is not None:  # type: ignore
            return self.patients.count()  # type: ignore
        return 0


class Inventory(models.Model):
    opd = models.OneToOneField(
        "Opd",
        on_delete=models.CASCADE,
        related_name="inventory",
        null=True,
        blank=True,  # NOTE: initally after updating we are going to remove it
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" Inventory of {str(self.opd.owner.name)}"


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
    gender_type = (
        ("male", "male"),
        ("female", "female"),
    )
    name = models.CharField("Full Name", max_length=200, null=True, blank=True)
    age = models.PositiveIntegerField("Age")
    gender = models.CharField("Gender", max_length=10, choices=gender_type, null=True)
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

    online_request_status = (
        ("seen", "seen"),
        ("not_seen", "not_seen"),
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
    status = models.CharField(
        "Status", max_length=20, choices=online_request_status, null=True
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

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.opd.no_of_appointment = models.F("no_of_appointment") + 1
            self.opd.save()
            self.opd.refresh_from_db()

    @transaction.atomic
    def delete(self, *args, **kwargs):  # type: ignore
        self.opd.no_of_appointment = models.F("no_of_appointment") - 1
        self.opd.save()
        self.opd.refresh_from_db()
        super().delete(*args, **kwargs)

    @property
    def name(self):
        if self.online_patient is not None:
            return self.online_patient.name
        return self.offline_patient.name


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

    # TODO: chagne the value of type based on the appointment automatically
    patient_type = models.CharField(
        "Patient Type", choices=type, max_length=30, null=True
    )
    patient_id = models.CharField("Patient ID", max_length=10, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField("Description", null=True)
    total_bill = models.DecimalField(
        "Total Bill", max_digits=10, decimal_places=2, null=True
    )
    billing_report = models.TextField("Bill Report", null=True)
    next_appointment = models.DateTimeField("Next Appointment Date", null=True)
    bed_reservation = models.PositiveIntegerField("Bed Reservation Hour", default=0)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = [["opd", "patient_id"]]

    def __str__(self):
        return str(self.patient_id)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self.opd.no_of_beds = models.F("no_of_beds") + 1
            self.opd.save()

    @transaction.atomic
    def delete(self, *args, **kwargs):  # type: ignore
        self.opd.no_of_beds = models.F("no_of_beds") - 1
        self.opd.save()
        super().delete(*args, **kwargs)

    @property
    def name(self):
        if self.online_patient is not None:
            return self.online_patient.name
        return self.offline_patient.name

    @property
    def type(self):
        if self.online_patient is not None:
            return "online"
        return "offline"

    @property
    def age(self):
        if self.online_patient is not None:
            return self.online_patient.age
        return self.offline_patient.age

    @property
    def gender(self):
        if self.online_patient is not None:
            return self.online_patient.gender
        return self.offline_patient.gender

    @property
    def address(self):
        if self.online_patient is not None:
            return self.online_patient.address
        return self.offline_patient.address

    @property
    def phone_number(self):
        if self.online_patient is not None:
            return self.online_patient.phone_number
        return self.offline_patient.phone_number

    @property
    def email(self):
        if self.online_patient is not None:
            return self.online_patient.email
        return self.offline_patient.email
