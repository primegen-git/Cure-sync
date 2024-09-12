# TODO: change the "date_of_appointment" -> date
# TODO: delete the unnecessary null = true from the field attribute
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
    address = models.TextField("Address")
    experience = models.PositiveIntegerField("Year of Experience", default=0)
    about = models.TextField(blank=True)
    education = models.TextField()
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


# NOTE: Opd is created automatically when the doctor is created through the django siganls
class Opd(models.Model):
    owner = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name="opd")
    name = models.CharField("Name", max_length=255)
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


# NOTE: inventory is created automatically when the doctor is created through the django siganls
class Inventory(models.Model):
    opd = models.OneToOneField(
        "Opd",
        on_delete=models.CASCADE,
        related_name="inventory",
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
    quantity = models.PositiveIntegerField("Quantity", default=0)
    price = models.DecimalField("Price", max_digits=10, default=0, decimal_places=2)

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        verbose_name_plural = "Inventory Items"

    def __str__(self):
        return f"{self.medicine}  in {self.inventory}"


class Offline_Patient(models.Model):
    gender_type = (
        ("male", "male"),
        ("female", "female"),
    )
    name = models.CharField("Full Name", max_length=200)
    age = models.PositiveIntegerField("Age")
    gender = models.CharField("Gender", max_length=10, choices=gender_type)
    email = models.EmailField("Email", max_length=190)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    display_id = models.CharField("ID", max_length=30)
    phone_number = models.CharField("Phone Number", max_length=10)
    address = models.TextField("Address")
    medical_history = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.name)


# TODO: learn how to combine the offline_patient and the online_patient together.
# TODO: once the above task is completed remove the status property
# NOTE: make a signal which increase or decrease if the no_of_appointment related to the particular opd
class Appointment(models.Model):
    online_request_status = (
        ("seen", "seen"),
        ("not_seen", "not_seen"),
    )

    opd = models.ForeignKey(Opd, on_delete=models.CASCADE, related_name="appointments")
    offline_patient = models.ForeignKey(
        Offline_Patient,
        on_delete=models.SET_NULL,  # offline patient can be deleted only from the appointment section.
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

    appointment_type = models.CharField("Appointment Type", max_length=30)
    status = models.CharField(
        "Status", choices=online_request_status, max_length=20, null=True, blank=True
    )
    appointment_id = models.CharField(
        "Appointment ID",
        max_length=10,
        unique=True,
    )
    date_of_appointment = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return str(self.appointment_id)

    class Meta:
        unique_together = [["opd", "online_patient"], ["opd", "offline_patient"]]

    @property
    def name(self):
        if self.online_patient:
            return self.online_patient.name
        return self.offline_patient.name


class Patient(models.Model):
    opd = models.ForeignKey(Opd, on_delete=models.CASCADE, related_name="patients")
    offline_patient = models.ForeignKey(
        Offline_Patient,
        on_delete=models.SET_NULL,
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

    # NOTE: handle in the signals file
    patient_type = models.CharField("Patient Type", max_length=30)
    patient_id = models.CharField("Patient ID", max_length=10, unique=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    description = models.TextField("Description")
    total_bill = models.DecimalField(
        "Total Bill", max_digits=10, decimal_places=2, default=0
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

    # TODO: find a way to handle all these property carefully
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
