from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["content", "author"]


@admin.register(Blog)
class ModelNameAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    inlines = [CommentInline]
