from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView
                                       )
from accounts.forms import CustomAuthenticationForm, EditProfileForm, CustomSignupForm
from accounts.models import Profile
from blog.models import Post


# Create your views here.

class CustomSignUpView(CreateView):
    model = User
    form_class = CustomSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('blog:post_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created. Now you can login')
        return response

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm
    redirect_field_name = 'next'

    def get_success_url(self):
        user = self.request.user
        messages.success(self.request, f'Welcome Back {user.username}!')
        next_url = self.request.GET.get(self.redirect_field_name)
        if next_url:
            return next_url
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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profile updated successfully')
        return response

class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')

class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'