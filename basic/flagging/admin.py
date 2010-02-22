from django.contrib import admin
from basic.flagging.models import *


class FlagTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(FlagType, FlagTypeAdmin)


class FlagAdmin(admin.ModelAdmin):
    list_display = ('object', 'flag_type')
    list_filter = ('flag_type',)
    raw_id_fields = ('user',)
admin.site.register(Flag, FlagAdmin)