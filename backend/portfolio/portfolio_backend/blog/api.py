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
    author_id = request.GET.get('author_id', '')  #the author id should be in query params, i.e. URL
    if author_id:
        blogs = blogs.filter(author_id=author_id)
    else:
        blogs = blogs.filter(viewable=True)


    serializer = BlogListSerializer(blogs, many=True)
    print(request.user)

    return Response({'data':serializer.data})

@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_view(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'data': 'Blog does not exist', 'success': False}, status=404)
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


def update_instance(instance, data, allowed_fields):
    for field, value in data.items():
        if field in allowed_fields and hasattr(instance, field):
            setattr(instance, field, value)
    instance.save()
    return instance

@api_view(['GET', 'PUT', 'FILES'])
@permission_classes([])
def blog_update(request, pk):
    blog = Blog.objects.get(pk=pk)
    if blog.author.id == request.user.id:
        if request.method == 'GET':
            serializer = BlogDetailSerializer(blog)
            return Response({'data':serializer.data})

        elif request.method == 'PUT':
            try:
                blog = Blog.objects.get(pk=pk)
            except Blog.DoesNotExist:
                return Response({'data': 'Blog does not exist', 'success': False}, status=404)

            allowed_fields = ['title', 'body', 'cover']
            try:
                update_data = request.data.copy()
                if 'cover' in update_data and request.FILES['cover']:
                    update_data['cover'] = request.FILES['cover']

                update_instance(blog, update_data, allowed_fields)
                serializer = BlogDetailSerializer(blog)
                return Response({'data': serializer.data, 'success': True})
            except Exception as e:
                print(e)
                return Response({'errors': e, 'success': False,}, status=400)
    else:
        return Response({'errors': 'Unauthorized Access', 'success': False,}, status=400)

@api_view(['POST'])
def tag_create(request):
    tag_form = TagForm(request.data, request.FILES)
    if tag_form.is_valid():
        tag_form.save()
        return Response({'success': True})
    else:
        print('errors', tag_form.errors, tag_form.non_field_errors())
        return Response({'errors': tag_form.errors.as_json(), 'success': False,}, status=400)
