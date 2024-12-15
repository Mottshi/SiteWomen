from django.db import models
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from slugify import slugify


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(is_published=Women.Status.PUBLISHED)



class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = AutoSlugField(populate_from="title", slugify_function=slugify, verbose_name="Slug")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    is_published = models.IntegerField(default=Status.DRAFT, choices=Status, verbose_name="Статус")
    cat = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name="Категория")
    tags = models.ManyToManyField("TagPost", related_name="women", blank=True, verbose_name="Теги")
    husband = models.OneToOneField("Husband", on_delete=models.SET_NULL, null=True, blank=True, related_name="wife", verbose_name="Муж")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", default=None, blank=True, null=True, verbose_name="Фото")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Изветсные женщины"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create']),
        ]
        db_table = 'women'

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = 'category'



class TagPost(models.Model):
    tag = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)


    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tag_slug": self.slug})

    class Meta:
        db_table = 'tag_post'



class Husband(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'husband'