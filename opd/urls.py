from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("login/", views.login_doctor, name="login"),
    path("logout/", views.logout_doctor, name="logout"),
    path("home/", views.home_page, name="home_page"),
    path("products/", views.product_list, name="product_list"),
    path("profile/", views.doctor_profile, name="doctor_profile"),
    path("profile/edit/", views.edit_doctor_profile, name="edit_doctor_profile"),
    path("appointment/", views.appointment, name="appointment"),
    path("confirmation_page/", views.confirmation_page, name="confirmation_page"),
    path("appointment_request/", views.appointment_request, name="appointment_request"),
    path("patient_report/<str:id>", views.patient_report, name="patient_report"),
    path("medicine/<str:id>", views.medicine, name="medicine"),
    path("add_product/", views.add_product, name="add_product"),
    path(
        "offline_appointment_booking/",
        views.offline_appointment_booking,
        name="offline_appointment_booking",
    ),
    path(
        "online_appointment_booking/<str:id>",
        views.online_appointment_booking,
        name="online_appointment_booking",
    ),
]
