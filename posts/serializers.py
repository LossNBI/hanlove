# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment, PostImage, PostVideo

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.nickname')
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']

    # 댓글 작성자의 ID를 추가로 반환
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_id'] = instance.author.id
        return representation

# 게시물에 포함될 이미지 시리얼라이저
class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']

# 게시물에 포함될 영상 시리얼라이저
class PostVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVideo
        fields = ['video']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.nickname')
    comments = CommentSerializer(many=True, read_only=True)
    
    # 중첩된 시리얼라이저를 사용하여 여러 이미지와 영상을 포함
    images = PostImageSerializer(many=True, read_only=True)
    videos = PostVideoSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        # 필드 목록에 'image'와 'video' 대신 'images'와 'videos'를 추가
        fields = ['id', 'author', 'caption', 'images', 'videos', 'created_at', 'comments']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_id'] = instance.author.id
        return representation