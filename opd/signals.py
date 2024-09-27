from django.db.models.signals import post_save, post_delete, pre_delete
from django.contrib.auth.models import Group
from django.dispatch import receiver
from .models import Doctor, Inventory, Opd, Appointment, Patient
from django.core.cache import cache
from django.db import models, transaction


def online_appointment_request(sender, instance, created, **kwargs):
    if created and instance.online_patient:
        cache_key = "some_value"
        appointments = Appointment.objects.filter(appointment_type="online")
        cache.set(cache_key, appointments, timeout=None)


def create_opd_and_inventory(sender, instance, created, **kwargs):
    if created:
        Opd.objects.create(owner=instance)
        Inventory.objects.create(opd=instance.opd)


def add_user_to_doctor_group(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        doctor_group = Group.objects.get(name="Doctor")
        user.groups.add(doctor_group)


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if not created:
        user.name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    user = instance.user
    user.delete()


def increment_appointment(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            opd = instance.opd
            opd.no_of_appointment = models.F("no_of_appointment") + 1
            opd.save()

            if instance.online_patient:
                instance.appointment_type = "online"
            else:
                instance.appointment_type = "offline"
            instance.save()


def decrement_appointment(sender, instance, **kwargs):
    with transaction.atomic():
        opd = instance.opd
        if not kwargs.get("raw", False):
            opd.no_of_appointment = models.F("no_of_appointment") - 1
            opd.save()


def increment_bed(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            opd = instance.opd
            opd.no_of_beds = models.F("no_of_beds") + 1
            opd.save()

            if instance.online_patient:
                instance.patient_type = "online"
            else:
                instance.patient_type = "offline"
            instance.save()


def decrement_bed(sender, instance, **kwargs):
    with transaction.atomic():
        opd = instance.opd
        opd.no_of_beds = models.F("no_of_beds") - 1
        opd.save()


@receiver(post_delete, sender=Patient)
def delete_offline_patient(sender, instance, **kwargs):
    with transaction.atomic():
        if instance.patient_type == "offline":
            instance.offline_patient.delete()


@receiver(post_delete, sender=Appointment)
def delete_offline_appointment(sender, instance, **kwargs):
    with transaction.atomic():
        if instance.appointment_type == "offline":
            instance.offline_patient.delete()


# save/create signals
post_save.connect(receiver=increment_appointment, sender=Appointment)
post_save.connect(receiver=add_user_to_doctor_group, sender=Doctor)
post_save.connect(receiver=updateUser, sender=Doctor)
post_save.connect(receiver=create_opd_and_inventory, sender=Doctor)
post_save.connect(receiver=increment_bed, sender=Patient)

# delete signals
post_delete.connect(receiver=deleteUser, sender=Doctor)
post_delete.connect(receiver=decrement_appointment, sender=Appointment)
post_delete.connect(receiver=decrement_bed, sender=Patient)
