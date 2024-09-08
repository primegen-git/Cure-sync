from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import Group
from .models import Doctor, Inventory, Opd, Appointment
from django.core.cache import cache


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


post_save.connect(receiver=add_user_to_doctor_group, sender=Doctor)
post_save.connect(receiver=updateUser, sender=Doctor)
post_save.connect(receiver=create_opd_and_inventory, sender=Doctor)
post_delete.connect(receiver=deleteUser, sender=Doctor)
