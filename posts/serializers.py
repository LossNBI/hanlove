# posts/serializers.py

from rest_framework import serializers
from .models import Post
from users.models import CustomUser

# 게시물 작성자의 닉네임을 보여주기 위한 Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['nickname']

# Post 모델을 위한 Serializer
class PostSerializer(serializers.ModelSerializer):
    # 'author' 필드를 읽기 전용으로 설정하고,
    # 중첩된 Serializer를 사용해 닉네임을 포함시킵니다.
    author = CustomUserSerializer(read_only=True) 

    class Meta:
        model = Post
        # 'author' 필드는 자동 생성되므로, 리스트에 포함시키지 않습니다.
        fields = ['id', 'author', 'caption', 'image', 'video', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']