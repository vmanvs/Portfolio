from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('useraccount.urls')),
    path('api/v1/blog/', include('blog.urls'))
]
