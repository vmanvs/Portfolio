from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/v1/auth/', include('useraccount.urls')),
    path('api/v1/blog/', include('blog.urls')),
    #path('kit/', include('auth_kit.urls')),
]
