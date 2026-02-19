from django.shortcuts import render


def home(request):
    return render(request, "portfolio/home.html")


def work(request):
    return render(request, "portfolio/work.html")
