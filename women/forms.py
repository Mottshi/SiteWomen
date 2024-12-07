from django import forms
from .models import Category, Husband, TagPost

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Имя", widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите имя'}))
    # slug = forms.SlugField(max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={"cols":50, "rows":5}), required=False, label="Введите описание")
    is_published = forms.BooleanField(required=False, label="Статус", initial=True)
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Выберите теги", required=False)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label="Не замужем")