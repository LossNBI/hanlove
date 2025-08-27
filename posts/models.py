# posts/models.py

from django.db import models
# 변경! Django 기본 User 모델 대신, 직접 만든 CustomUser를 가져옵니다.
from users.models import CustomUser 

class Post(models.Model):
    # 변경! ForeignKey가 CustomUser를 참조하도록 합니다.
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    caption = models.TextField()
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'