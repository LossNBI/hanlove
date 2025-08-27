# posts/views.py

from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    # 모든 게시물을 불러옵니다. 최신 게시물을 가장 먼저 보여주기 위해 -created_at을 사용합니다.
    queryset = Post.objects.all().order_by('-created_at')
    # 게시물 데이터를 JSON으로 변환할 Serializer를 지정합니다.
    serializer_class = PostSerializer
    # 로그인된 사용자만 게시물을 작성할 수 있도록 권한을 설정합니다.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 

    def perform_create(self, serializer):
        # 새로운 게시물이 생성될 때, 작성자(author)를 현재 로그인된 사용자로 자동 설정합니다.
        # 이렇게 하면 사용자가 직접 author 정보를 입력할 필요가 없습니다.
        serializer.save(author=self.request.user)