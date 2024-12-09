from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband, TagPost


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = "russian"

    def __init__(self, message=None):
        self.message = message if message else "Должны присуствовать только русские символы, дефис и пробел"

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)




class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Имя", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}),
                            error_messages={
                                "min_length": "Заголовок слишком короткий",
                                "required": "Без заголовка никак",
                                            },
                            validators=[
                                RussianValidator(),
                            ])
    # slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={"cols":50, "rows":5}), required=False, label="Введите описание")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Выберите теги", required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем")
    str().isascii()