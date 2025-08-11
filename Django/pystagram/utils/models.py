from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField("작석일자", auto_now_add=True)
    updated_at = models.DateTimeField("수정일자", auto_now=True)

    class Meta:
        abstract = True
