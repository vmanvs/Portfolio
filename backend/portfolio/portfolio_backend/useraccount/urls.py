from django.urls import path
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenVerifyView
from . import  views

urlpatterns = [
    path('', views.home),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
]