from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes, authentication_classes

from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'tags', 'cover_url', 'author')


