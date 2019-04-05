from django.urls import path, re_path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    re_path(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    re_path(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    re_path(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tags'),
    path('index', views.IndexView.as_view(), name='index'),
    path('about', views.about, name='about'),
    path('projects', views.ProjIndexView.as_view(), name='projects'),
    re_path(r'^project/(?P<pk>[0-9]+)/$', views.ProjDetailView.as_view(), name='proj_detail'),
]