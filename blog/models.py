from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags

# Create your models here.


def default_cat():
    return Category.objects.get_or_create(name='Default')[0].pk


class Category(models.Model):
    """
    post category
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    post tag
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    posts
    """
    title = models.CharField(max_length=120)
    excerpt = models.CharField(max_length=1000, blank=True)
    body = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(Category, default=default_cat, on_delete=models.SET_DEFAULT)
    tags = models.ManyToManyField(Tag, blank=True)

    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'mdx_math'
            ],
                extension_configs={
                    'mdx_math': {'enable_dollar_delimiter': True}
                }
            )
            self.excerpt = strip_tags(md.convert(self.body))[:100]
        super(Post, self).save(force_insert=False, force_update=False, using=None, update_fields=None)

    def prev(self):
        try:
            pr = self.get_previous_by_created_time()
            return [pr]
        except self.DoesNotExist:
            return []

    def next(self):
        try:
            nx = self.get_next_by_created_time()
            return [nx]
        except self.DoesNotExist:
            return []


class Project(models.Model):
    name = models.CharField(max_length=120)
    created_time = models.DateField()
    skills = models.ManyToManyField(Tag)
    intro = models.TextField()
    body = models.TextField()
    link = models.CharField(max_length=200)
    image = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:proj_detail', kwargs={'pk': self.pk})
