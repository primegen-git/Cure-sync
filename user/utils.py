from django.contrib.auth import authenticate

from opd.models import Doctor, Opd


def custom_authenticate(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)

    if user is not None:
        if user.groups.filter(name="Profile").exists():  # type: ignore
            return user
    return None


def check_user(request):
    if request.user and request.user.groups.filter(name="Profile").exists():
        return request.user
    return None


def search_specialist_doctor(request, search_query):
    return Doctor.objects.filter(speciality__icontains=search_query)  # type:ignore


def search_by_opd(request, search_query):
    return Opd.objects.filter(name__icontains=search_query)
