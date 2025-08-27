# posts/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

# PostViewSet은 기존 그대로 둡니다.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # URL에서 'post_id'를 가져와서 해당 게시물의 댓글만 필터링합니다.
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('created_at')

    def perform_create(self, serializer):
        # URL에서 'post_id'를 가져와서 해당 게시물에 댓글을 연결하고,
        # 작성자를 현재 로그인된 사용자로 설정합니다.
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post, author=self.request.user)