from django.contrib import admin
from basic.music.models import *


class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Genre, GenreAdmin)


class LabelAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Label, LabelAdmin)


class BandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Band, BandAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display  = ('title', 'band',)
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Album, AlbumAdmin)


class TrackAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Track, TrackAdmin)