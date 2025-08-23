# notice/views.py

from rest_framework import generics
from .models import Notice
from .serializers import NoticeSerializer

class NoticeListAPIView(generics.ListAPIView):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer