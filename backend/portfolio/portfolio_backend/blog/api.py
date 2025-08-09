from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .forms import BlogForm, TagForm
from rest_framework.response import Response

from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_list_view(request):
    blogs = Blog.objects.all()
    serializer = BlogListSerializer(blogs, many=True)
    print(request.user)

    return Response({'data':serializer.data})

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_view(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    serializer = BlogDetailSerializer(blog, many=False)

    return Response({'data':serializer.data})


@api_view(['POST', 'FILES'])
@permission_classes([])
def blog_create(request):
    blog_form = BlogForm(request.data, request.FILES)
    if blog_form.is_valid():
        form = blog_form.save(commit=False)
        form.author = request.user
        form.save()
        return Response({'success': True})
    else:
        print('errors', blog_form.errors, blog_form.non_field_errors())
        return Response({'errors': blog_form.errors.as_json(), 'success': False,}, status=400)

@api_view(['POST'])
def tag_create(request):
    tag_form = TagForm(request.data, request.FILES)
    if tag_form.is_valid():
        tag_form.save()
        return Response({'success': True})
    else:
        print('errors', tag_form.errors, tag_form.non_field_errors())
        return Response({'errors': tag_form.errors.as_json(), 'success': False,}, status=400)
