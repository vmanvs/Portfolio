from django.urls import path
from . import  api

urlpatterns = [
    path('', api.blog_list_view, name='blog_list'),
    path('<uuid:pk>/', api.blog_view, name='blog_detail'),
    path('create/', api.blog_create, name='blog_create'),
    path('<uuid:pk>/update/', api.blog_update, name='blog_update'),
]