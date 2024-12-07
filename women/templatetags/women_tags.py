from django import template
from django.db.models import Count
import women.views as views

from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(posts__gt=0)
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("women/list_tag.html")
def show_tags(post=None):
    if post:
        tags = post.tags.all()
    else:
        tags = TagPost.objects.annotate(total=Count("women")).filter(women__gt=0)
    return {"tags": tags}