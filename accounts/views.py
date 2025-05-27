from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from accounts.forms import CustomAuthenticationForm


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
    success_url = reverse_lazy('blog:post_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')