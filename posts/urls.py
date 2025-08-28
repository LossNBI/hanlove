# posts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 게시물 목록 조회 및 생성 API
    path('', views.PostListCreateView.as_view(), name='post-list-create'),

    # 특정 게시물 조회, 수정, 삭제 API (새로 추가)
    path('<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # 특정 게시물에 대한 댓글 목록 조회 및 생성 API
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),

    # 특정 댓글 조회, 수정, 삭제 API (새로 추가)
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]