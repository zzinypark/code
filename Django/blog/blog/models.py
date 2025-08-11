from io import BytesIO

from PIL import Image
from pathlib import Path
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import models

from utils.models import TimeStampedModel

User = get_user_model()


class Blog(TimeStampedModel):
    CATEGORY_CHOICES = (
        ("free", "자유"),
        ("travel", "여행"),
        ("cat", "고양이"),
        ("dog", "개"),
    )
    category = models.CharField(
        "카테고리", max_length=20, choices=CATEGORY_CHOICES, default="free"
    )
    title = models.CharField("제목", max_length=50)
    content = models.TextField("본문")
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    image = models.ImageField(
        "이미지", null=True, blank=True, upload_to="blog/%Y/%m/%d"
    )
    thumbnail = models.ImageField(
        "썸네일", null=True, blank=True, upload_to="blog/%Y/%m/%d/thumbnail"
    )

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title[:10]}"

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"blog_pk": self.pk})

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300, 300))

        image_path = Path(self.image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix.lower()
        thumbnail_filename = f"{thumbnail_name}_thumb{thumbnail_extension}"

        if thumbnail_extension in [".jpg", "jpeg"]:
            file_type = "JPEG"
        elif thumbnail_extension == ".gif":
            file_type = "GIF"
        elif thumbnail_extension == ".png":
            file_type = "PNG"
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "블로그"
        verbose_name_plural = "블로그 목록"


# 제목
# 본문
# 작성자 - 일단패스
# 작성일자
# 수정일자
# 카테고리


class Comment(TimeStampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.CharField("본문", max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.blog.title} 댓글"

    class Meta:
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ("-create_at", "-id")

    # blog
    # content
    # user
    # create_at
    # update_at
