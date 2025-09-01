# posts/views.py

from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from .models import Post, Comment, PostImage, PostVideo
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrAdmin, IsCommentAuthorOrAdmin
from django.db import transaction

# 게시물 목록 조회 및 생성
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser] # 이 라인을 추가하여 파일 업로드를 가능하게 합니다.

    def perform_create(self, serializer):
        with transaction.atomic():
            # Post 객체를 먼저 생성합니다.
            post = serializer.save(author=self.request.user)

            # 요청 데이터에서 'images' (또는 'image') 파일을 가져옵니다.
            images = self.request.FILES.getlist('image')
            for image_file in images:
                PostImage.objects.create(post=post, image=image_file)

            # 요청 데이터에서 'videos' (또는 'video') 파일을 가져옵니다.
            videos = self.request.FILES.getlist('video')
            for video_file in videos:
                PostVideo.objects.create(post=post, video=video_file)

# 특정 게시물 조회, 수정, 삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrAdmin]

# 특정 게시물에 대한 댓글 목록 조회 및 생성
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return self.queryset.filter(post_id=post_id)
        
    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(pk=post_id)
        serializer.save(post=post, author=self.request.user)

# 특정 댓글 조회, 수정, 삭제
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrAdmin]