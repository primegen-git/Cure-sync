from django.contrib.auth.models import Group, User


def add_user_to_doctor_group(user):
    doctor_group = Group.objects.get(name="Doctor")
    user.groups.add(doctor_group)


def create_doctor_user(username, password, email):
    user = User.objects.create_user(username=username, password=password, email=email)
    add_user_to_doctor_group(user)
    return user


def is_doctor(user):
    return user.groups.filter(name="Doctor").exists()
