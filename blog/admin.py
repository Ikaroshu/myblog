from django.contrib import admin
from .models import Post, Category, Tag, Project
from martor.widgets import AdminMartorWidget
from django.db import models


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMartorWidget},
    # }
    list_display = ['title', 'created_time', 'modified_time', 'category']


class ProjectAdmin(admin.ModelAdmin):
    # formfield_overrides = {
    #     models.TextField: {'widget': AdminMartorWidget},
    # }
    list_display = ['name', 'created_time']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Project, ProjectAdmin)
