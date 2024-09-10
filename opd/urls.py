from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("login/", views.login_doctor, name="login"),
    path("logout/", views.logout_doctor, name="logout"),
    path("home/", views.home_page, name="home_page"),
    path("products/", views.product_list, name="product_list"),
    path("profile/", views.doctor_profile, name="doctor_profile"),
    path("appointment/", views.appointment, name="appointment"),
    path("appointment_request/", views.appointment_request, name="appointment_request"),
    path("patient_report/<str:id>", views.patient_report, name="patient_report"),
]
