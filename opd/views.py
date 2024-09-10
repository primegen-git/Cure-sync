from django.contrib import messages
from django.http import HttpResponseForbidden
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from opd.models import Doctor, Appointment
from opd.utils import (
    get_product_count,
    is_doctor,
    get_processed_data,
    custom_authenticate,
)
from django.db.models import Q


def login_doctor(request):
    if request.method == "POST":
        user = custom_authenticate(request)
        if user is None:
            messages.error(request, "something wrong in either username or password")
            return redirect("opd:login")
        login(request, user)
        messages.success(request, "successfull login")
        return redirect("opd:home_page")

    context = {}
    return render(request, "opd/doctor_login.html", context)


def logout_doctor(request):
    logout(request)
    messages.success(request, "you have been logout successfully")
    return redirect("opd:login")


@user_passes_test(is_doctor, login_url="home:home_page")
def home_page(request):
    opd = request.user.doctor.opd
    patients = opd.patients.all().order_by("-date")
    context = {"opd": opd, "patients": patients}
    return render(request, "opd/patient.html", context)


@user_passes_test(is_doctor, login_url="home:home_page")
def product_list(request):
    products = request.user.doctor.opd.inventory.inventory_items.all()
    count = get_product_count(products)[0]
    context = {"products": products, "count": count}
    return render(request, "opd/product.html", context)


@user_passes_test(is_doctor, login_url="home:home_page")
def doctor_profile(request):
    doctor = request.user.doctor
    context = {"doctor": doctor}
    return render(request, "opd/doctor_profile.html", context)


@user_passes_test(is_doctor, login_url="home:home_page")
def appointment(request):
    appointments = request.user.doctor.opd.appointments.filter(
        Q(offline_patient__isnull=False)
        | Q(online_patient__isnull=False, status="seen")
    )
    request_count = request.user.doctor.opd.appointments.filter(
        Q(online_patient__isnull=False, status="not_seen")
    ).count()
    total_appointment = len(appointments)
    context = {
        "appointments": appointments,
        "total_appointment": total_appointment,
        "request_count": request_count,
    }
    return render(request, "opd/appointment.html", context)


@user_passes_test(is_doctor, login_url="home:home_page")
def appointment_request(request):
    search_query = request.GET.get("search_query")
    appointment_id = request.GET.get("id")
    print(search_query)
    print(appointment_id)
    if search_query and appointment_id:
        print("inside the if statement")
        try:
            appointment = request.user.doctor.opd.appointments.get(id=appointment_id)
            if search_query == "accepted":
                appointment.status = "seen"
                appointment.save()
            elif search_query == "cancel":
                appointment.delete()
            else:
                return HttpResponseBadRequest("Invalid search query")
            return redirect("opd:appointment")
        except Appointment.DoesNotExist:
            return HttpResponseBadRequest("Appointment does not exist")
    appointments = request.user.doctor.opd.appointments.filter(
        Q(online_patient__isnull=False, status="not_seen")
    )
    context = {"appointments": appointments}
    return render(request, "opd/online_appointment_request.html", context)


@user_passes_test(is_doctor, login_url="home:home_page")
def patient_report(request, id):
    patient = request.user.doctor.opd.patients.get(id=id)  # type: ignore
    context = {"patient": patient}
    return render(request, "opd/patient_report.html", context)
