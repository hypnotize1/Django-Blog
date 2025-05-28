from django.urls import path
from .views import (CustomLogoutView,
                    CustomLoginView,
                    CustomSignUpView,
                    UserProfileView,
                    UserProfileUpdateView
                    )


app_name = 'accounts'
urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name = 'signup' ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit'),

]