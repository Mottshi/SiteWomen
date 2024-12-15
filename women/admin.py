from django.contrib import admin, messages
from django.db.models.functions import Length
from django.utils.safestring import mark_safe

from .models import Women, Category


# Register your models here.
#Кастомный фильтр
class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"


    #то что на отображается указывает на первом индексе, то что отправляется на сервер на втором
    def lookups(self, request, model_admin):
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    #то, как фильто будет работать на queryset и что по итогу вернет
    def queryset(self, request, queryset):
        match self.value():
            case "married":
                return queryset.filter(husband__isnull=False)
            case "single":
                return queryset.filter(husband__isnull=True)


@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ("title", "content", "slug", "cat", "husband", "tags", "photo", "post_photo") #отображаемые поля для редактирования
    readonly_fields = ("slug", "post_photo") #поля только для чтения
    filter_horizontal = ("tags", )#добавление тегов в режиме редактирования
    list_display = ("title", "post_photo", "time_create", "is_published", "cat")#отображаемые поля в просмотре
    list_display_links = ("title", )#кликабельные поля в просмотре
    ordering = ("time_create", "title")#сортировка
    list_editable = ("is_published",)#редактируемые поля в просмотре
    list_per_page = 5#кол-во отображаемых записей
    actions = ["set_published", "set_draft"]#добавление кастомных действий
    search_fields = ("title", "cat__name")#поля для поиска
    list_filter = ("is_published", "cat__name", MarriedFilter) #добавление фильтров
    save_on_top = True


    #добавляет новое поле
    @admin.display(description="Изображения")
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src=\"{women.photo.url}\" width=50>")
        return ""


    #добавляет новое дествией над таблицей
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Измененно {count} записей")

    @admin.action(description="Снять выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Измененно {count} записей", messages.WARNING)





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


admin.site.site_header = 'Панель администрирования'
admin.site.index_title = 'Известные женщины мира'