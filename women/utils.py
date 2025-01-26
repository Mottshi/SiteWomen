from django.views.generic.base import ContextMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'users:login'}
]


class DataMixin(ContextMixin):
    paginate_by = 2
    page_title = None
    cat_selected = None


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.page_title:
            context["title"] = self.page_title
        if self.cat_selected is not None:
            context["cat_selected"] = self.cat_selected
        return context

