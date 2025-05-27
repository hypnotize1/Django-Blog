from django.urls import path
from .views import CustomLogoutView, CustomLoginView, CustomSignUpView

app_name = 'accounts'

urlpatterns = [
    path('signup/', CustomSignUpView.as_view(), name = 'signup' ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]