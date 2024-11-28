from django import template
import women.views as views

from women.models import Category, TagPost

register = template.Library()


@register.inclusion_tag("women/list_categories.html")
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag("women/list_tag.html")
def show_tags(post=None):
    if post:
        tags = post.tags.all()
    else:
        tags = TagPost.objects.all()
    return {"tags": tags}