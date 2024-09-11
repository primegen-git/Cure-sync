from functools import wraps
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from django.forms import models
from django.db import models
from opd.models import (
    Appointment,
    Inventory_Item,
    Medicine,
    Offline_Patient,
    Opd,
    Doctor,
    Patient,
)
from django.db.models import Q


def add_user_to_doctor_group(user):
    doctor_group = Group.objects.get(name="Doctor")
    user.groups.add(doctor_group)


def create_doctor_user(username, password, email):
    user = User.objects.create_user(username=username, password=password, email=email)
    add_user_to_doctor_group(user)
    return user


def is_doctor(user):
    return user.groups.filter(name="Doctor").exists()


def get_processed_data(patients):
    return [
        patient.offline_patient if patient.type == "offline" else patient.online_patient
        for patient in patients
    ]


def get_product_count(products):
    return [sum(product.quantity for product in products)]


def get_total_bed_count():
    opds = Opd.objects.all()
    total_beds = 0
    for opd in opds:
        total_beds += opd.no_of_beds
    return total_beds


def get_total_doctor_count():
    return Doctor.objects.count()


def get_total_appointment_count():
    return Appointment.objects.count()


def custom_authenticate(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None and user.groups.filter(name="Doctor").exists():
        return user

    return None


def appointment_handler(id):
    appointment = Appointment.objects.get(id=id)
    appointment.opd.no_of_appointment = models.F("no_of_appointment") - 1
    appointment.delete()


def product_handler(id):
    product = Inventory_Item.objects.get(id=id)
    product.delete()


def patient_handler(id):
    patient = Patient.objects.get(id=id)
    patient.opd.no_of_appointment = models.F("no_of_appointment") - 1
    patient.delete()


def search_product(request, search_query):
    return request.user.doctor.opd.inventory.inventory_items.filter(
        Q(medicine__name__icontains=search_query)
        | Q(medicine__category__icontains=search_query)
    )


def search_appointment(request, search_query):
    appointments = Appointment.objects.filter(opd=request.user.doctor.opd)
    appointments = appointments.filter(
        Q(appointment_id__icontains=search_query)
        | Q(offline_patient__name__icontains=search_query)
        | Q(online_patient__name__icontains=search_query)
    )

    return appointments


def search_patient(request, search_query):
    patients = Patient.objects.filter(opd=request.user.doctor.opd)
    patients = patients.filter(
        Q(patient_id__icontains=search_query)
        | Q(online_patient__name__icontains=search_query)
        | Q(offline_patient__name__icontains=search_query)
        | Q(offline_patient__gender__icontains=search_query)
        | Q(offline_patient__gender__icontains=search_query)
        | Q(patient_type__icontains=search_query)
    )

    return patients
