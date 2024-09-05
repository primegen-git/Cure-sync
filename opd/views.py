from django.shortcuts import render


def home_page(request):
    context = {}
    return render(request, "opd/patient.html", context)


def employee_list(request):
    context = {}
    return render(request, "opd/employee.html", context)


def product_list(request):
    context = {}
    return render(request, "opd/product.html", context)


def doctor_profile(request):
    context = {}
    return render(request, "opd/doctor_profile.html", context)
