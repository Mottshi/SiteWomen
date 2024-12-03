from django.contrib import admin, messages
from django.db.models.functions import Length

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
    list_display = ("title", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title", )
    ordering = ("time_create", "title")
    list_editable = ("is_published",)
    list_per_page = 5
    actions = ["set_published", "set_draft"]
    search_fields = ("title", "cat__name")
    list_filter = ("is_published", "cat__name", MarriedFilter) #добавление фильтров


    #добавляет новое поле
    @admin.display(description="Краткое описание", ordering=Length("content"))
    def brief_info(self, women: Women):
        return f"Описание {len(women.content)} символов"


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