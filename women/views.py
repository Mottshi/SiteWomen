from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404


# Create your views here.
def index(request) -> HttpResponse:
    return HttpResponse("Страница приложения women.")


def categories(request, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id:{cat_id}</p>")


def categories_by_slug(request, cat_slug: str) -> HttpResponse:
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug:{cat_slug}</p>")


def archive(request, year: int) -> HttpResponse:
    if year > 2024:
        raise Http404()
    return HttpResponse(f"<h1>Архив по годам</h1><p>year:{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")