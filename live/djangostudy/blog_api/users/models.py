from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # 추가 필드 예시
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]  # ORM 최적화 베스트 프랙티스
        indexes = [models.Index(fields=["username"])]  # 인덱스 추가
