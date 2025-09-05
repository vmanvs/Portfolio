from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.db.models import Q
from .forms import BlogForm, TagForm
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from .models import Blog
from .serializers import BlogListSerializer, BlogDetailSerializer


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def blog_list_view(request):
    #blogs = Blog.objects.all()
    author_id = request.GET.get('author_id', '')  #the author id should be in query params, i.e. URL
    tags_raw = request.GET.get('tags', None)
    page_size = int(request.GET.get('limit', '10'))
    offset = int(request.GET.get('offset', '0'))
    if author_id:
        blogs = Blog.objects.filter(Q(author_id=author_id) & Q(deleted=False))[offset:offset+page_size]

    elif tags_raw:
        tags = tags_raw.split('-') if tags_raw else []

        if tags:
            query = Q()
            for value in tags:
                query |= Q(tags__name_icontains=value)
            try:
                blogs = Blog.objects.filter(query, viewable=True)[offset:offset + page_size]  # check this function
            except ObjectDoesNotExist:
                return Response({'data': 'No such blog', 'success': False}, status=404)

    else:
        blogs = Blog.objects.filter(viewable=True)[offset:offset+page_size] #check this function

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

@api_view(['GET'])
def blog_delete(request, pk):
    try:
        blog = Blog.objects.get(pk=pk)
    except Blog.DoesNotExist:
        return Response({'data': 'Blog does not exist', 'success': False}, status=404)

    if request.user == blog.author:
        blog.deleted = True
        blog.viewable = False
        blog.save()
        return Response({'success': True}, status=200)
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




