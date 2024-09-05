from django.db.models.signals import post_save, post_delete

from django.contrib.auth.models import User
from .models import Doctor


def createDoctorProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Doctor.objects.create(  # type: ignore
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email,
        )


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


post_save.connect(receiver=createDoctorProfile, sender=User)
post_save.connect(receiver=updateUser, sender=Doctor)
post_delete.connect(receiver=deleteUser, sender=Doctor)
