from django.http import JsonResponse
from nbformat.v1.nbjson import JSONReader
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import BlogForm
from rest_framework.permissions import IsAuthenticated

from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_list_view(request):
    blogs = Blog.objects.all()
    serializer = BlogListSerializer(blogs, many=True)

    return JsonResponse({'data':serializer.data}, safe=False)

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    serializer = BlogDetailSerializer(blog, many=False)

    return JsonResponse({'data':serializer.data}, safe=False)


@api_view(['POST', 'FILES'])
@permission_classes([])
@authentication_classes([])
def blog_create(request):
    blog_form = BlogForm(request.data, request.FILES)
    if blog_form.is_valid():
        form = blog_form.save(commit=False)
        form.author = request.user
        form.save()
        return JsonResponse({'success': True})
    else:
        print('errors', blog_form.errors, blog_form.non_field_errors())
        return JsonResponse({'errors': blog_form.errors.as_json(), 'success': False,}, status=400, safe=False)
