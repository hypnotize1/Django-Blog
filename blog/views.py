from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView

from .forms import PostCreateForm
from .models import *


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(is_published=True).order_by('-created_at')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self):
        post_pk = self.kwargs.get('post_pk')
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, pk=post_pk, slug=post_slug)
        Post.objects.filter(pk=post.pk).update(views=F('views') + 1)
        post.refresh_from_db()
        return post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
