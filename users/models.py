# users/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # AbstractUser가 제공하는 username, password, is_staff 필드에 더해
    # nickname 필드를 추가합니다.
    nickname = models.CharField(max_length=150, unique=False, blank=True, null=True)

    def __str__(self):
        return self.username