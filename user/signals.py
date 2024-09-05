from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.conf import settings
from .models import Profile


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(  # type: ignore
            user=user,
            name=user.first_name,
            username=user.username,
            email=user.email,
        )

        # subject = "welcome to DevSearch"
        # message = f"hi {profile.name}, we are glad you are here"
        #
        # send_mail(
        #     subject,
        #     message,
        #     settings.EMAIL_HOST_USER,
        #     [profile.email],
        #     fail_silently=False,
        # )


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


post_save.connect(receiver=createProfile, sender=User)
post_save.connect(receiver=updateUser, sender=Profile)
post_delete.connect(receiver=deleteUser, sender=Profile)
