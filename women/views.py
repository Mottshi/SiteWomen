from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse


# Create your views here.
def index(request) -> HttpResponse:
    # t = render_to_string("women/index.html")
    return render(request,"women/index.html")


def categories(request, cat_id: int) -> HttpResponse:
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id:{cat_id}</p>")


def categories_by_slug(request, cat_slug: str) -> HttpResponse:
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug:{cat_slug}</p>")


def archive(request, year: int) -> HttpResponse:
    if year > 2024:
        uri = reverse("cats", args=("music",))
        return redirect(uri)
    return HttpResponse(f"<h1>Архив по годам</h1><p>year:{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def about(request):
    return render(request, "women/about.html")