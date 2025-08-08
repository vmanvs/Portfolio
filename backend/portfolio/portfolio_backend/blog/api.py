from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated

from .models import Blog
from .serializers import BlogSerializer


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_list_view(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)

    return JsonResponse({'data':serializer.data})
