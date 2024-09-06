from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from opd.models import Doctor, Inventory


def login_page(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                user.doctor  # type: ignore
            except AttributeError:
                return HttpResponseForbidden("You don't have access to view this page")
            login(request, user)
            messages.success(request, "successfull login")
            return redirect("opd:home_page")
        else:
            messages.error(request, "login failed")
            return redirect("opd:login")

    context = {}
    return render(request, "opd/doctor_login.html", context)


def home_page(request):
    context = {}
    return render(request, "opd/patient.html", context)


@login_required(login_url="opd:login")
def product_list(request):
    # try:
    #     doctor = request.user.doctor
    #     products = .objects.filter(owner=doctor)
    # except AttributeError:
    #     return HttpResponseForbidden("you don't have a doctor account")
    # context = {"products": products}
    context = {}
    return render(request, "opd/product.html", context)


@login_required(login_url="opd:login")
def doctor_profile(request):
    try:
        doctor = request.user.doctor
    except AttributeError:
        return HttpResponseForbidden("you don't have access to this account")
    context = {"doctor": doctor}
    return render(request, "opd/doctor_profile.html", context)


@login_required(login_url="opd:login")
def appointment(request):
    context = {}
    return render(request, "opd/appointment.html", context)


@login_required(login_url="opd:login")
def appointment_request(request):
    context = {}
    return render(request, "opd/online_appointment_request.html", context)
