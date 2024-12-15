from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse
from django.template.defaultfilters import slugify
from .forms import *
import uuid
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


def handle_uploaded_file(f):
    with open(f"uploads/{uuid.uuid4()}_{f.name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
# Create your views here.
def index(request) -> HttpResponse:
    posts = Women.published.all().select_related("cat")
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        "cat_selected": 0,
    }
    return render(request, "women/index.html", context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")



def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data["file"])
    else:
        form = UploadFileForm()
    data = {"title": "О сайте", "menu": menu, "form": form}
    return render(request, "women/about.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }
    return render(request, "women/post.html", context=data)


def addpage(request):
    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # try:
            #     tags = form.cleaned_data.pop("tags")
            #     new_woman = Women.objects.create(**form.cleaned_data)
            #     new_woman.tags.set(tags)
            #     return redirect("home")
            # except:
            #     form.add_error(None, "Ошибка заполнения формы")
            form.save()
            return redirect("home")
    else:
        form = AddPostForm()
    data = {
        "menu": menu,
        "title": "Добавление статьи",
        "form": form
    }
    return render(request, "women/addpage.html", context=data)


def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = category.posts.filter(is_published=1)
    data = {
        "title": f"Рубрика {category.name}",
        "menu": menu,
        "posts": posts,
        "cat_selected": category.pk,
    }
    return render(request, "women/index.html", context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.women.filter(is_published=Women.Status.PUBLISHED).select_related("cat")
    data = {
        "title": f"Тег {tag.tag}",
        "menu": menu,
        "posts": posts,
        "cat_selected": None,
    }

    return render(request, "women/index.html", context=data)




