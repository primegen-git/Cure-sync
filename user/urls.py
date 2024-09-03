from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("beds/", views.bed_list, name="bed_list"),
    path("hospitals/", views.hospital_list, name="hospital_list"),
]
