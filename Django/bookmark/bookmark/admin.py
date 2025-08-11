from django.contrib import admin
from bookmark.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "created_at"]
    list_display_links = ["name", "url"]
    list_filter = ["name", "url"]


# admin.site.register(Bookmark, BookmarkAdmin)
