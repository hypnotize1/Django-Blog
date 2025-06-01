from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import F
from django.shortcuts import redirect
from django.template.defaultfilters import title
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView
from django.core.paginator import Paginator
from django.contrib import messages

from .forms import PostCreateForm, CommentCreateForm, PostSearchForm
from .models import *


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        query_set = Post.objects.filter(is_published=True).select_related('author').order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            query_set = query_set.filter(title__icontains=query)
        return query_set

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = PostSearchForm(self.request.GET)
        return context
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments_list = Comment.objects.filter(post=self.object, approved=True).select_related('author')
        paginator = Paginator(comments_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj
        context['comment_form'] = CommentCreateForm()
        return context

    def get_object(self):
        post = Post.objects.prefetch_related('categories', 'tags').get(
            pk=self.kwargs['post_pk'],
            slug=self.kwargs['post_slug'],
        )
        Post.objects.filter(pk = post.pk).update(views=F('views') + 1)
        post.refresh_from_db()
        return post

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = self.object
            new_comment.author = request.user
            new_comment.save()
            messages.success(request, 'Your comment has been successfully submitted and will be displayed after approval. ')
            return redirect(self.object.get_absolute_url())

        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])
        messages.success(self.request, 'Post successfully created.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        messages.success(self.request, 'Post successfully updated.')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return self.object.get_absolute_url()

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post successfully deleted.')
        return super().delete(request, *args, **kwargs)
