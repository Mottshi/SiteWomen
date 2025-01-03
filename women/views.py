from typing import Any

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .utils import DataMixin

from .forms import *
import uuid
from .models import Women, Category, TagPost



def handle_uploaded_file(f):
    with open(f"uploads/{uuid.uuid4()}_{f.name}", 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
# Create your views here.


class WomenHomeView(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"
    page_title = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        queryset = Women.objects.all().select_related("cat")
        return queryset


class AddPageView(DataMixin, CreateView):
    form_class = AddPostForm
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    page_title = "Добавление статьи"



class UpdatePageView(DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    page_title = "Редактирование статьи"


class DeletePageView(DataMixin, DeleteView):
    model = Women
    template_name = "women/deletepage.html"
    context_object_name = "post"
    success_url = reverse_lazy("home")
    page_title = "Удаление статьи"



class WomenCategoryView(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs["cat_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs["cat_slug"])
        context = super().get_context_data(title=f"Категория {category.name}",
                                           cat_selected=category.pk)
        return context


class ShowTagPostListView(DataMixin, ListView):
    model = Women
    context_object_name = "posts"
    template_name = "women/index.html"

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs["tag_slug"]).select_related("cat")

    def get_context_data(self, **kwargs):
        tag = get_object_or_404(TagPost, slug=self.kwargs["tag_slug"])
        context = super().get_context_data(title=tag.tag)
        return context


class ShowPostView(DataMixin, DetailView):
    template_name = "women/post.html"
    slug_url_kwarg = "post_slug"
    context_object_name = "post"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(title=self.object.title)
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
    data = {"title": "О сайте", "form": form}
    return render(request, "women/about.html", context=data)



def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")






