from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path
from .views import (CustomLogoutView,
                    CustomLoginView,
                    CustomSignUpView,
                    UserProfileView,
                    UserProfileUpdateView,
                    UserPasswordResetView,
                    UserPasswordResetDoneView,
                    UserPasswordResetConfirmView,
                    UserPasswordResetCompleteView
                    )


app_name = 'accounts'
urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name = 'signup' ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit'),

    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]

