from django.contrib import messages
import json
from django.http import HttpResponseForbidden, HttpResponseServerError
from django.http.response import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from opd.forms import (
    InventoryItemsForm,
    OfflinePatientAppointmentForm,
    OnlinePatientAppointmentForm,
    DoctorProfileForm,
)
from opd.models import Doctor, Appointment, InventoryItem, Patient
from opd.utils import (
    get_product_count,
    is_doctor,
    get_processed_data,
    custom_authenticate,
    appointment_handler,
    product_handler,
    patient_handler,
    search_appointment,
    search_patient,
    search_product,
    create_patient,
)
from django.db.models import Q
from django.db import models
import logging

logger = logging.getLogger(__name__)


def login_doctor(request):
    try:
        if request.method == "POST":
            user = custom_authenticate(request)
            if user is None:
                messages.error(
                    request, "something wrong in either username or password"
                )
                return redirect("opd:login")
            login(request, user)
            messages.success(request, "successfull login")
            return redirect("opd:home_page")
        context = {}
        return render(request, "opd/doctor_login.html", context)
    except Exception as e:
        logger.error(f"Error in login_doctor: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def logout_doctor(request):
    try:
        logout(request)
        messages.success(request, "you have been logout successfully")
        return redirect("opd:login")
    except Exception as e:
        logger.error(f"Error in logout_doctor: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def home_page(request):
    try:
        search_query = request.GET.get("search_query", "")
        opd = request.user.doctor.opd
        if search_query:
            patients = search_patient(request, search_query)
        else:
            patients = opd.patients.all().order_by("-date")
        context = {"opd": opd, "patients": patients}
        return render(request, "opd/patient.html", context)
    except Exception as e:
        logger.error(f"Error in home_page: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def product_list(request):
    try:
        search_query = request.GET.get("search_query", "")
        if search_query:
            products = search_product(request, search_query)
        else:
            products = request.user.doctor.opd.inventory.inventory_items.all()
        count = get_product_count(products)[0]  # type: ignore
        context = {"products": products, "count": count}  # type: ignore
        return render(request, "opd/product.html", context)
    except Exception as e:
        logger.error(f"Error in product_list: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def doctor_profile(request):
    try:
        doctor = request.user.doctor
        context = {"doctor": doctor}
        return render(request, "opd/doctor_profile.html", context)
    except Exception as e:
        logger.error(f"Error in doctor_profile: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )

@user_passes_test(is_doctor, login_url="home:home_page")
def edit_doctor_profile(request):
    try:
        doctor = request.user.doctor
        if request.method == "POST":
            form = DoctorProfileForm(request.POST, request.FILES, instance=doctor)
            if form.is_valid():
                form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect("opd:doctor_profile")
        else:
            form = DoctorProfileForm(instance=doctor)
        context = {"form": form}
        return render(request, "opd/form/edit_doctor_profile.html", context)
    except Exception as e:
        logger.error(f"Error in edit_doctor_profile: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later.")


@user_passes_test(is_doctor, login_url="home:home_page")
def appointment(request):
    try:
        search_query = request.GET.get("search_query", "")
        if search_query:
            appointments = search_appointment(request, search_query)
            # Set request_count and total_appointment to default values in search mode
            request_count = 0
            total_appointment = appointments.count()
        else:
            appointments = request.user.doctor.opd.appointments.filter(
                Q(offline_patient__isnull=False)
                | Q(patient_profile__isnull=False, status="seen")
            )
            request_count = request.user.doctor.opd.appointments.filter(
                Q(patient_profile__isnull=False, status="not_seen")
            ).count()
            total_appointment = request.user.doctor.opd.appointments.filter(
                status="seen"
            ).count()
        context = {
            "appointments": appointments,
            "total_appointment": total_appointment,
            "request_count": request_count,
        }
        return render(request, "opd/appointment.html", context)
    except Exception as e:
        logger.error(f"Error in appointment: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def appointment_request(request):
    try:
        search_query = request.GET.get("search_query")
        appointment_id = request.GET.get("id")
        if search_query and appointment_id:
            try:
                appointment = request.user.doctor.opd.appointments.get(
                    id=appointment_id
                )
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
                    Q(patient_profile__isnull=False, status="not_seen")
        )
        context = {"appointments": appointments}
        return render(request, "opd/online_appointment_request.html", context)
    except Exception as e:
        logger.error(f"Error in appointment_request: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def patient_report(request, id):
    try:
        patient = request.user.doctor.opd.patients.get(id=id)  # type: ignore
        context = {"patient": patient}
        return render(request, "opd/patient_report.html", context)
    except Exception as e:
        logger.error(f"Error in patient_report: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def confirmation_page(request):
    try:
        confirmation = request.GET.get("confirmation")
        section = request.GET.get("section")
        id = request.GET.get("id")
        if confirmation == "yes":
            if section and id:
                if section == "appointment":
                    appointment_handler(id)
                    messages.success(
                        request, "Appointment has been successfully deleted."
                    )
                    return redirect("opd:appointment")
                if section == "product":
                    product_handler(id)
                    messages.success(request, "Product has been successfully deleted.")
                    return redirect("opd:product_list")
                if section == "patient":
                    patient_handler(id)
                    messages.success(request, "Patient has been successfully deleted.")
                    return redirect("opd:home_page")
            else:
                return redirect("opd:home_page")

        if confirmation == "no":
            if section == "appointment":
                return redirect("opd:appointment")
            if section == "product":
                return redirect("opd:product_list")
            if section == "patient":
                return redirect("opd:home_page")

        context = {"section": section, "id": id}
        return render(request, "opd/confirmation_page.html", context)
    except Exception as e:
        logger.error(f"Error in confirmation_page: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def offline_appointment_booking(request):
    try:
        if request.method == "POST":
            opd = request.user.doctor.opd
            form = OfflinePatientAppointmentForm(request.POST)
            if form.is_valid():
                form.save(opd=opd)
                return redirect("opd:appointment")
        form = OfflinePatientAppointmentForm()
        context = {"form": form}
        return render(request, "opd/form/offline_appointment.html", context)
    except Exception as e:
        logger.error(f"Error in offline_appointment_booking: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def online_appointment_booking(request, id):
    try:
        if request.method == "POST":
            opd = request.user.doctor.opd
            form = OnlinePatientAppointmentForm(request.POST)
            if form.is_valid():
                appointment = Appointment.objects.get(id=id)
                appointment.opd = opd
                appointment.patient_type = "online"
                appointment.appointment_id = request.POST["appointment_id"]
                appointment.appointment_date = request.POST["appointment_date"]
                appointment.save()
                messages.success(request, "Appointment is successfully added")
                return redirect("opd:appointment")
            else:
                messages.error(request, "something wrong in the form")
                return redirect("opd:online_appointment_booking", id=id)
        else:
            form = OnlinePatientAppointmentForm()
        context = {}
        return render(request, "opd/form/online_appointment_booking.html", context)
    except Exception as e:
        logger.error(f"Error in online_appointment_booking: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def medicine(request, id):
    try:
        if request.method == "POST":
            medication_data_json = request.POST.get("medicationData", "[]")
            medication_list = json.loads(medication_data_json)

            updated_medication_list = []
            medicine_description = []

            for medication in medication_list:
                name = medication["name"]
                requested_quantity = int(medication["quantity"])
                medicine_description.append(f"{name}: {requested_quantity}")

                try:
                    inventory_item = InventoryItem.objects.filter(
                        inventory=request.user.doctor.opd.inventory, name=name
                    ).first()

                    if inventory_item:
                        available_quantity = inventory_item.quantity
                        if requested_quantity <= available_quantity:
                            inventory_item.quantity = (
                                models.F("quantity") - requested_quantity
                            )
                            inventory_item.save()
                        else:
                            available_quantity = (
                                inventory_item.quantity
                            )  # Keep original if insufficient
                    else:
                        available_quantity = 0

                except InventoryItem.DoesNotExist:
                    available_quantity = 0

                updated_medication_list.append(
                    {
                        "name": name,
                        "requested_quantity": requested_quantity,
                        "available_quantity": available_quantity,
                    }
                )

            context = {"medications": updated_medication_list}
            appointment = Appointment.objects.get(id=id)

            # Create the medicine description string
            medicine_details = "Prescribed Medicines:\n" + "\n".join(
                medicine_description
            )

            patient = create_patient(request, id)
            patient.description = medicine_details
            patient.save()
            appointment.delete()

            return render(request, "opd/form/medicine_report.html", context)

        context = {}
        return render(request, "opd/form/medicine.html", context)
    except Exception as e:
        logger.error(f"Error in medicine: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


@user_passes_test(is_doctor, login_url="home:home_page")
def add_product(request):
    try:
        if request.method == "POST":
            form = InventoryItemsForm(request.POST)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.inventory = request.user.doctor.opd.inventory
                instance.save()
                messages.success(request, "Product has been added")
                return redirect("opd:product_list")
            else:
                messages.error(request, "Something is wrong in the form")
                return redirect("opd:add_product")
        form = InventoryItemsForm()
        context = {"form": form}
        return render(request, "opd/form/product.html", context)
    except Exception as e:
        logger.error(f"Error in add_product: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )
