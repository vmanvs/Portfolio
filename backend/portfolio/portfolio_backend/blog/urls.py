from django.urls import path
from . import  api

urlpatterns = [
    path('', api.blog_list_view, name='blog_list'),
]