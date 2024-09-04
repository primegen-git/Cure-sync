from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
