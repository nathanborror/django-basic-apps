from django.contrib import admin
from basic.bookmarks.models import *


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('url', 'description')
    search_fields = ('url', 'description', 'extended')

admin.site.register(Bookmark, BookmarkAdmin)