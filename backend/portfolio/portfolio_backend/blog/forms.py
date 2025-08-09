from django.forms import ModelForm
from .models import Blog, Tag


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = (
            'title',
            'body',
            'tags',
            'cover',

        )


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
