from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from .forms import *
import uuid
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

default_context = {
    "title": "Главная страница",
    'menu': menu,
    'cat_selected': 0,
}


def handle_uploaded_file(f):
    with open(f"uploads/{uuid.uuid4()}_{f.name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
# Create your views here.


class WomenHomeView(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = default_context.copy()

    def get_queryset(self):
        queryset = Women.objects.all().select_related("cat")
        return queryset


class AddPageView(CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = default_context.copy()
    extra_context["title"] = "Добавление статьи"



class UpdatePageView(UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    extra_context = default_context.copy()
    extra_context["title"] = "Редактирование статьи"


class DeletePageView(DeleteView):
    model = Women
    template_name = "women/deletepage.html"
    context_object_name = "post"
    success_url = reverse_lazy("home")
    extra_context = default_context.copy()
    extra_context["title"] = "Удаление статьи"



class WomenCategoryView(ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    extra_context = default_context.copy()
    extra_context["title"] = "Главная страница"

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        context["title"] = "Категория - " + category.name
        context["cat_selected"] = category.pk
        return context


class ShowTagPostListView(ListView):
    model = Women
    context_object_name = "posts"
    template_name = "women/index.html"
    extra_context = default_context.copy()
    extra_context["title"] = "Главная страница"

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagPost, slug=self.kwargs["tag_slug"])
        context["title"] = tag.tag
        return context


class ShowPostView(DetailView):
    # model = Women
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"
    extra_context = default_context.copy()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.title
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data["file"])
    else:
        form = UploadFileForm()
    data = {"title": "О сайте", "menu": menu, "form": form}
    return render(request, "women/about.html", context=data)



def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")






