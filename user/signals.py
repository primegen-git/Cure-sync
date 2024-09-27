from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import Group, User
from .models import Profile


def create_profile(sender, instance, created, **kwargs):
    # idea here is to create a profile when the user is save and its group is Profile
    if created:
        if instance.groups.filter(name="Profile").exists():
            Profile.objects.create(
                user=instance,
                name=instance.first_name,
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


post_save.connect(receiver=create_profile, sender=User)
post_save.connect(receiver=updateUser, sender=Profile)
post_delete.connect(receiver=deleteUser, sender=Profile)
