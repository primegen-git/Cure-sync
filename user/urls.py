from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("beds/", views.bed_list, name="bed_list"),
    path("hospitals/", views.hospital_list, name="hospital_list"),
    path("hospital/", views.hospital_detail, name="hospital_detail"),
    path("search_specialist/", views.search_specialist, name="search_specialist"),
    path("chatbot/", views.chatbot, name="chatbot"),
]
