from django.urls import path
from .views import UserRegister, UserProfileUpdateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', obtain_auth_token, name='login'),
    path('profile', UserProfileUpdateView.as_view(), name='profile'),
]
