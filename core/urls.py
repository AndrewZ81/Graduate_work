from django.urls import path
from .views import RegisterUserView, LoginView, ProfileView, ChangePasswordView

urlpatterns = [
    path('signup', RegisterUserView.as_view(), name='signup'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('update_password', ChangePasswordView.as_view(), name='update_password'),
]
