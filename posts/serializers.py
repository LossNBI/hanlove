# posts/serializers.py

from rest_framework import serializers
from .models import Post, Comment

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


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.nickname')
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'caption', 'image', 'video', 'created_at', 'comments']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author_id'] = instance.author.id
        return representation