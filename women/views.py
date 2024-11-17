from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

data_db = [{'id': 1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
           {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
           {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': False}, ]


# Create your views here.
def index(request) -> HttpResponse:
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": data_db,
    }
    return render(request, "women/index.html", context=data)


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
    data = {"title": "О сайте"}
    return render(request, "women/about.html", context=data)
