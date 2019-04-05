from django import template
from ..models import Post, Category, Tag
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag
def get_recent_posts(num=3):
    return Post.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def get_archives():
    return Post.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.filter(name='prange')
def prange(number):
    return range(number-3 if number-3 > 0 else 1, number+4)


@register.filter(name='right_bound')
def right_bound(number):
    return number+3


@register.filter(name='left_bound')
def left_bound(number):
    return number-3


@register.filter(name='left_right')
def left_right(bl):
    return not bl
