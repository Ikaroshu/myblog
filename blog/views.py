from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag, Project
from comments.forms import CommentForm
import markdown
from django.views.generic import ListView, DetailView

# Create your views here.


def home(request):
    post_list = Post.objects.all().order_by('-created_time')[:3]
    proj_list = Project.objects.all().order_by('-created_time')[:4]
    return render(request, 'blog/home.html', context={
        'post_list': post_list,
        'proj_list': proj_list
    })


def about(request):
    return render(request, 'blog/about.html')


class IndexView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'
    ordering = ['-created_time']
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'All Posts'
        return context


class ProjIndexView(ListView):
    model = Project
    template_name = 'blog/project_index.html'
    context_object_name = 'project_list'
    ordering = ['-created_time']
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['page_title'] = 'All Projects'
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'mdx_math'
        ],
            extension_configs={
                'mdx_math': {'enable_dollar_delimiter': True}
            }
        )
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context


class ProjDetailView(DetailView):
    model = Project
    template_name = 'blog/project_detail.html'
    context_object_name = 'proj'

    def get_object(self, queryset=None):
        proj = super().get_object()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'mdx_math'
        ],
            extension_configs={
                'mdx_math': {'enable_dollar_delimiter': True}
            }
        )
        proj.body = md.convert(proj.body)
        return proj


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/home.html', context={
        'post_list': post_list
    })


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)

    def get_context_data(self, *, object_list=None, **kwargs):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        context = super(IndexView, self).get_context_data()
        context['page_title'] = cate.name
        return context


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)

    def get_context_data(self, *, object_list=None, **kwargs):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        context = super(IndexView, self).get_context_data()
        context['page_title'] = tag.name
        return context
