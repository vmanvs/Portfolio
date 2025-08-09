from django.urls import path
from . import  api

urlpatterns = [
    path('', api.blog_list_view, name='blog_list'),
    path('<int:pk>/', api.blog_view, name='blog_detail'),
    path('create/', api.blog_create, name='blog_create'),
]