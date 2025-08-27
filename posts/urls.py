from django.urls import path
from . import views

urlpatterns = [
    # 게시물에 대한 댓글 목록 조회 및 생성 API
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),
]