# hanlove/notice/urls.py

from django.urls import path
from .views import NoticeListCreateView, NoticeDetailView

urlpatterns = [
    # 공지사항 목록 조회 (GET)
    path('list/', NoticeListCreateView.as_view(), name='notice-list'),
    # 공지사항 생성 (POST)
    path('create/', NoticeListCreateView.as_view(), name='notice-create'),
    # 특정 공지사항 상세 조회, 업데이트, 삭제
    path('<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]