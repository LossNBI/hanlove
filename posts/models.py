# posts/models.py

from django.db import models
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} - {self.caption[:30]}'

# 하나의 게시물에 여러 이미지를 연결하기 위한 모델
class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')
    
    def __str__(self):
        return f'Image for Post {self.post.id}'

# 하나의 게시물에 여러 영상을 연결하기 위한 모델
class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='post_videos/')
    
    def __str__(self):
        return f'Video for Post {self.post.id}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post}'