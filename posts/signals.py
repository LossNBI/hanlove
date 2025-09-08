# community/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Post

@receiver(post_delete, sender=Post)
def auto_delete_images_on_post_delete(sender, instance, **kwargs):
    """
    게시글(Post)이 삭제될 때, 연결된 모든 이미지 파일도 함께 삭제합니다.
    """
    for image in instance.images.all():
        image.delete()