from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.
def index(request) -> HttpResponse:
    return HttpResponse("Страница приложения women.")

def categories(request) -> HttpResponse:
    return HttpResponse("<h1>Статьи по категориям</h1>")


