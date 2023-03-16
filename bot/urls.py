from django.urls import path
from bot import views

urlpatterns = [
        path('verify', views.TgUserView.as_view(), name='user_verify'),
]
