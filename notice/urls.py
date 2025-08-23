# hanlove_final/notice/urls.py

from django.urls import path
from .views import NoticeListCreateView, NoticeDetailView

urlpatterns = [
    # 공지사항 목록 조회 및 생성 (POST 요청 시 관리자만 가능)
    path('notices/', NoticeListCreateView.as_view(), name='notice-list-create'),
    # 특정 공지사항 삭제 (DELETE 요청 시 관리자만 가능)
    path('notices/<int:pk>/', NoticeDetailView.as_view(), name='notice-detail'),
]

