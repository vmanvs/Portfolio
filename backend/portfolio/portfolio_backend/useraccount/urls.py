from django.urls import path
from dj_rest_auth.views import LoginView
from rest_framework_simplejwt.views import TokenVerifyView
from .views import custom_tokens

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify/', TokenVerifyView.as_view(), name='verify'),
    path('tokens/', custom_tokens, name='custom_tokens'),
]