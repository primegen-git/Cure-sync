from django.urls import path
from . import views


app_name = "hospital"
urlpatterns = [
    path("hospital/", views.hospital_detail, name="hospital_detail"),
]
