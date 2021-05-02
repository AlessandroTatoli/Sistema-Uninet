from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "home.html")


def flujograma(request):
    return render(request, "flujograma.html")
