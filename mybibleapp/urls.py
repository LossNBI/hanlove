# mybibleapp/urls.py

"""
URL configuration for mybibleapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

# DRF 라우터를 사용하기 위해 추가
from rest_framework.routers import DefaultRouter
from posts.views import PostViewSet

# DRF 라우터를 사용해 posts 앱의 URL을 자동으로 생성합니다.
router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/notices/', include('notice.urls')),
    
    # 이 부분을 추가합니다. 기존 API 경로와 충돌하지 않도록 'api/' 아래에 라우터를 포함합니다.
    path('api/', include(router.urls)),
]