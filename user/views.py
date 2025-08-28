from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.http import HttpResponseServerError

import logging

from opd.models import Appointment, Doctor, Opd
from opd.utils import (
    get_total_appointment_count,
    get_total_bed_count,
    get_total_doctor_count,
)
from user.models import Profile
from user.utils import (
    appointment_count_and_id,
    check_user,
    custom_authenticate,
    get_appointment,
    getResponse,
    search_by_opd,
    search_specialist_doctor,
)

from .forms import CustomUserCreationForm, ProfileCreationForm

logger = logging.getLogger(__name__)


def user_login(request):
    try:
        if request.method == "POST":
            is_user = custom_authenticate(request)
            if is_user:
                login(request, is_user)
                return redirect("user:home_page")
            messages.error(request, "something wrong with user or password")
            return redirect("user:login")
        context = {}
        return render(request, "user/user_login.html", context)
    except Exception as e:
        logger.error(f"Error in user_login: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def user_logout(request):
    try:
        logout(request)
        messages.success(request, "you have been logout")
        return redirect("user:home_page")
    except Exception as e:
        logger.error(f"Error in user_logout: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def signup(request):
    try:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()

                messages.success(request, "user has been successfully created")
                login(request, user)
                return redirect("user:edit_profile")
            else:
                messages.error(request, "Some error occurs in the form submission")
                return redirect("user:signup")
        else:
            form = CustomUserCreationForm()

        context = {"form": form}
        return render(request, "signup.html", context)
    except Exception as e:
        logger.error(f"Error in signup: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def home_page(request):
    try:
        is_user = check_user(request)
        count = None
        user_appointment_id = None
        query = appointment_count_and_id(request)
        if query is not None:
            count = query[0]
            user_appointment_id = query[1]
        if is_user:
            context = {
                "user": is_user,
                "total_beds_count": get_total_bed_count,
                "total_doctor_count": get_total_doctor_count,
                "total_appointment_count": get_total_appointment_count,
                "appointments": get_appointment(request),
                "count": count,
                "user_appointment_id": user_appointment_id,
            }
            return render(request, "user/logged/profile.html", context)
        context = {
            "total_beds_count": get_total_bed_count,
            "total_doctor_count": get_total_doctor_count,
            "total_appointment_count": get_total_appointment_count,
        }
        return render(request, "user/index.html", context)
    except Exception as e:
        logger.error(f"Error in home_page: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def edit_profile(request):
    try:
        if request.method == "POST":
            form = ProfileCreationForm(
                request.POST, request.FILES, instance=request.user.profile
            )
            if form.is_valid():
                form.save()
                messages.success(request, "Profile has been successfully created")
                return redirect("user:user_profile")
            messages.error(request, "Some error occur in form submission")
            return redirect("user:edit_profile")
        else:
            form = ProfileCreationForm(instance=request.user.profile)

        context = {"form": form}
        return render(request, "user/edit_profile.html", context)
    except Exception as e:
        logger.error(f"Error in edit_profile: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def profile(request):
    try:
        context = {}
        return render(request, "user/profile.html", context)
    except Exception as e:
        logger.error(f"Error in profile: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def bed_list(request):
    try:
        is_user = check_user(request)
        if is_user:
            base_template = "user/logged/index.html"
        else:
            base_template = "base.html"
        sort = request.GET.get("sort")
        if sort == "beds":
            doctors = Doctor.objects.all().order_by("-opd__no_of_beds")
        else:
            doctors = Doctor.objects.all()
        context = {"doctors": doctors, "base_template": base_template}
        return render(request, "user/bed_list.html", context)
    except Exception as e:
        logger.error(f"Error in bed_list: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def opd_list(request):
    try:
        is_user = check_user(request)
        search = False
        if is_user:
            base_template = "user/logged/index.html"
        else:
            base_template = "base.html"
        search_query = request.GET.get("search_query", "")
        if search_query:
            opd = search_by_opd(request, search_query)
            doctors = opd.owner  # type: ignore
            search = True
        else:
            doctors = Doctor.objects.all()
        context = {"doctors": doctors, "base_template": base_template, "search": search}
        return render(request, "user/opd_list.html", context)
    except Exception as e:
        logger.error(f"Error in opd_list: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def hospital_detail(request):
    try:
        context = {}
        return render(request, "user/hospital_detail.html", context)
    except Exception as e:
        logger.error(f"Error in hospital_detail: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def search_specialist(request):
    try:
        is_user = check_user(request)
        if is_user:
            base_template = "user/logged/index.html"
        else:
            base_template = "base.html"
        search_query = request.GET.get("search_query", "")
        if search_query:
            doctors = search_specialist_doctor(request, search_query)
        else:
            doctors = Doctor.objects.all()
        context = {"doctors": doctors, "base_template": base_template}
        return render(request, "user/search_specialist.html", context)
    except Exception as e:
        logger.error(f"Error in search_specialist: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def chatbot(request):
    try:
        user_message = request.GET.get("message", "")
        if user_message:
            bot_response = getResponse(user_message)
        else:
            bot_response = ""
        context = {"bot_response": bot_response, "user_message": user_message}
        return render(request, "user/chatbot.html", context)
    except Exception as e:
        logger.error(f"Error in chatbot: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def appointment(request, pk):
    try:
        doctor = Doctor.objects.get(id=pk)
        search_query = request.GET.get("search_query")
        if search_query == "booking":
            is_user = check_user(request)
            if is_user:
                try:
                    Appointment.objects.create(
                        opd=Opd.objects.get_or_create(owner=doctor)[0],  # Ensure OPD exists safely
                        patient_profile=request.user.profile,
                        status="not_seen",
                    )
                    doctor.opd.save()
                    messages.success(
                        request, "You appoinment request has been send successfully"
                    )
                    return redirect("user:home_page")
                except Exception as e:
                    logger.error(f"Error creating appointment: {e}", exc_info=True)
                    messages.error(request, f"Error creating appointment")
                    return redirect("user:appointment", pk=doctor.id)
            return redirect("user:login")
        total_bed_count = doctor.opd.no_of_beds  # type: ignore
        total_appointment_count = doctor.opd.no_of_appointment  # type: ignore
        context = {
            "doctor": doctor,
            "total_appointment_count": total_appointment_count,
            "total_bed_count": total_bed_count,
        }
        return render(request, "user/appointment.html", context)
    except Exception as e:
        logger.error(f"Error in appointment: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def doctor_profile(request, pk):
    try:
        doctor = Doctor.objects.get(id=pk)
        context = {"doctor": doctor}
        return render(request, "user/doctor_profile.html", context)
    except Exception as e:
        logger.error(f"Error in doctor_profile: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def message(request):
    try:
        profile = Profile.objects.get(user=request.user)
        accepted = False
        doctor = None
        appointment = profile.get_appointment()
        if appointment is not None:
            doctor = profile.get_opd().owner  # type: ignore
            if appointment.status == "seen":
                accepted = True
        context = {"doctor": doctor, "appointment": appointment, "accepted": accepted}
        return render(request, "user/logged/message.html", context)
    except Exception as e:
        logger.error(f"Error in message: {e}", exc_info=True)
        return HttpResponseServerError(
            "An unexpected error occurred. Please try again later."
        )


def user_profile(request):
    try:
        is_user = check_user(request)
        context = {"user": is_user.profile}  # type: ignore
        return render(request, "user/logged/user_profile.html", context)
    except Exception as e:
        logger.error(f"Error in user_profile: {e}", exc_info=True)
        return HttpResponseServerError("An unexpected error occurred. Please try")
