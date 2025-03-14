from django.urls import path
from .views import UserLoginAPIView, UserRegisterAPIView, UserLogoutAPIView, RoleAPIView

app_name = 'users'

urlpatterns = [
    path('login', UserLoginAPIView.as_view(), name='login'),
    path('register', UserRegisterAPIView.as_view(), name='register'),
    path('logout', UserLogoutAPIView.as_view(), name='logout'),
    path('roles', RoleAPIView.as_view(), name='roles')
]
