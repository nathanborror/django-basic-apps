from django.contrib import admin
from basic.flagging.models import *


class FlagTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('content_type',)
admin.site.register(FlagType, FlagTypeAdmin)


class FlagAdmin(admin.ModelAdmin):
    list_display = ('object', 'flag_type')
    list_filter = ('flag_type',)
admin.site.register(Flag, FlagAdmin)