from django.contrib import admin
from basic.books.models import *


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Genre, GenreAdmin)


class PublisherAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Publisher, PublisherAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display  = ('title', 'pages')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Book, BookAdmin)


class HighlightAdmin(admin.ModelAdmin):
    list_display  = ('book', 'highlight')
    list_filter   = ('book',)
admin.site.register(Highlight, HighlightAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('book', 'current_page')
admin.site.register(Page, PageAdmin)