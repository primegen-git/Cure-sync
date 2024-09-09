from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("beds/", views.bed_list, name="bed_list"),
    path("opds/", views.opd_list, name="opd_list"),
    path("hospital/", views.hospital_detail, name="hospital_detail"),
    path("search_specialist/", views.search_specialist, name="search_specialist"),
    path("chatbot/", views.chatbot, name="chatbot"),
    path("appoinment/<str:pk>", views.appointment, name="appointment"),
    path("doctor/<str:pk>", views.doctor_profile, name="doctor_profile"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]
