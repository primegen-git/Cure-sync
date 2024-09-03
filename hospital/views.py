from django.shortcuts import render

# Create your views here.


def hospital_detail(request):
    context = {}
    return render(request, "hospital/hospital_detail.html", context)
