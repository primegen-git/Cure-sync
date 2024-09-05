from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("employees/", views.employee_list, name="employee_list"),
    path("products/", views.product_list, name="product_list"),
]
