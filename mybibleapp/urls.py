# mybibleapp/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings .
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/notices/', include('notice.urls')),
    path('api/posts/', include('posts.urls')),
]

# **이 부분을 추가해야 합니다.**
# 개발 환경에서 미디어 파일을 제공하도록 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)