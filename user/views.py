from django.shortcuts import render
from opd.models import Doctor
# Create your views here.


def home_page(request):
    context = {}
    return render(request, "user/index.html", context)


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
    context = {"doctor": doctor}
    return render(request, "user/appointment.html", context)


def doctor_profile(request, pk):
    doctor = Doctor.objects.get(id=pk)
    context = {"doctor": doctor}
    return render(request, "user/doctor_profile.html", context)
