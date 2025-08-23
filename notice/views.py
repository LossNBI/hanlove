# hanlove_final/notice/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Notice
from .serializers import NoticeSerializer

# 공지사항 목록 조회 및 생성 API
# 관리자만 생성 가능
class NoticeListCreateView(generics.ListCreateAPIView):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer

    def get_permissions(self):
        # 공지사항 조회(GET)는 인증된 모든 사용자가 가능
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        # 공지사항 생성(POST)은 관리자만 가능
        return [IsAdminUser()]

# 공지사항 상세 조회, 업데이트, 삭제 API
# 관리자만 업데이트와 삭제 가능
class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    # 삭제(DELETE)는 관리자만 가능
    permission_classes = [IsAdminUser]