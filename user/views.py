from django.shortcuts import render

# Create your views here.


def home_page(request):
    context = {}
    return render(request, "user/index.html", context)


def bed_list(request):
    context = {}
    return render(request, "user/bed_list.html", context)


def hospital_list(request):
    context = {}
    return render(request, "user/hospital_list.html", context)


def hospital_detail(request):
    context = {}
    return render(request, "user/hospital_detail.html", context)


def search_specialist(request):
    context = {}
    return render(request, "user/search_specialist.html", context)


def chatbot(request):
    context = {}
    return render(request, "chatbot.html", context)
