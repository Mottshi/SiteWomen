from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse

menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


# Create your views here.
def index(request) -> HttpResponse:
    # t = render_to_string("women/index.html")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "str": "lol",
        "float": 1.235,
        "set": {1, 2, 3, 4, 5},
        "dict": {"key_1": "value_1", "key_2": "value_2"},
        "obj": MyClass(10, 12)
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
