from django.urls import path
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import  GoogleLogin

urlpatterns = [
    path('token/google/', GoogleLogin.as_view(), name='google_login'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
]