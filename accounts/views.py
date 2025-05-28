from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from accounts.forms import CustomAuthenticationForm, EditProfileForm
from accounts.models import Profile
from blog.models import Post


# Create your views here.

class CustomSignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('blog:post_list')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('blog:post_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class UserProfileView(LoginRequiredMixin, ListView):
    """Displays user profile and their posts"""
    model = Post
    template_name = 'accounts/user_profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get_or_create(user=self.request.user)[0]  # Uses profile property
        return context

class UserProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Handles profile updates"""
    model = Profile
    form_class = EditProfileForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'accounts/edit_profile.html'

    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]

    def test_func(self):
        return self.request.user == self.get_object().user