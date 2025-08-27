# mybibleapp/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/notices/', include('notice.urls')),
    
    # 이 부분을 추가합니다. 기존 API 경로와 충돌하지 않도록 'api/' 아래에 라우터를 포함합니다.
    path('api/posts/', include('posts.urls')),
]