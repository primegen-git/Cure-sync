from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from opd.models import Doctor
from opd.utils import (
    get_total_appointment_count,
    get_total_bed_count,
    get_total_doctor_count,
)
from user.utils import custom_authenticate, check_user
# TODO: remove the message after a time


def user_login(request):
    if request.method == "POST":
        is_user = custom_authenticate(request)
        if is_user:
            login(request, is_user)
            messages.success(request, "Welcome back")
            return redirect("user:home_page")
        messages.error(request, "something wrong with user or password")
        return redirect("user:login")
    context = {}
    return render(request, "user/user_login.html", context)


def user_logout(request):
    logout(request)
    messages.success(request, "you have been logout")
    return redirect("user:home_page")


def home_page(request):
    # check if the home page is for user or not
    is_user = check_user(request)
    if is_user:
        context = {"user": is_user}
        return render(request, "user/logged/profile.html", context)
    context = {
        "total_beds_count": get_total_bed_count,
        "total_doctor_count": get_total_doctor_count,
        "total_appointment_count": get_total_appointment_count,
    }
    return render(request, "user/index.html", context)


def profile(request):
    context = {}
    return render(request, "user/profile.html", context)


def bed_list(request):
    doctors = Doctor.objects.all()
    context = {"doctors": doctors}
    return render(request, "user/bed_list.html", context)


def opd_list(request):
    doctors = Doctor.objects.all()
    context = {"doctors": doctors}
    return render(request, "user/opd_list.html", context)


def hospital_detail(request):
    context = {}
    return render(request, "user/hospital_detail.html", context)


def search_specialist(request):
    doctors = Doctor.objects.all()
    context = {"doctors": doctors}
    return render(request, "user/search_specialist.html", context)


def chatbot(request):
    context = {}
    return render(request, "chatbot.html", context)


def appointment(request, pk):
    doctor = Doctor.objects.get(id=pk)
    total_bed_count = doctor.opd.no_of_beds  # type: ignore
    total_appointment_count = doctor.opd.no_of_appointment  # type: ignore
    context = {
        "doctor": doctor,
        "total_appointment_count": total_appointment_count,
        "total_bed_count": total_bed_count,
    }
    return render(request, "user/appointment.html", context)


def doctor_profile(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {"doctor": doctor}
    return render(request, "user/doctor_profile.html", context)


# NOTE: All the method after this are related to the logged in user
