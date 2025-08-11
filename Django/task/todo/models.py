from io import BytesIO

from django.contrib.auth import get_user_model
from django.db import models
from PIL import Image
from pathlib import Path

User = get_user_model()


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_image = models.ImageField(
        null=True, blank=True, upload_to="todo/%Y/%m/%d"
    )
    thumbnail = models.ImageField(
        null=True,
        blank=True,
        upload_to="todo/%Y/%m/%d/thumbnail",
        default="todo/default.jpg",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.completed_image:
            return super().save(*args, **kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((100, 100))

        image_path = Path(self.completed_image.name)

        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f"{thumbnail_name}_thumbnail{thumbnail_extension}"

        if thumbnail_extension in [".jpg", ".jpeg"]:
            file_type = "JPEG"
        elif thumbnail_extension == ".png":
            file_type = "PNG"
        elif thumbnail_extension == ".gif":
            file_type = "GIF"
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, format=file_type)
        temp_thumb.seek(0)

        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)

        temp_thumb.close()
        return super().save(*args, **kwargs)


class Comment(models.Model):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.todo.title} 댓글"
