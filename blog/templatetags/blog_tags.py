from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
   # return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_tags=Count('post')).filter(num_tags__gt=0)
    # return Tag.objects.all()
