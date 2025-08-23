# notice/urls.py

from django.urls import path
from .views import NoticeListAPIView

urlpatterns = [
    path('notices/', NoticeListAPIView.as_view(), name='notice-list'),
]