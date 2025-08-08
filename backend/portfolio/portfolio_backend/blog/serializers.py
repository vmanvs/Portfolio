from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Blog


class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title','tags', 'cover_url', 'author')

class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title','slug', 'tags', 'body', 'cover_url', 'author')