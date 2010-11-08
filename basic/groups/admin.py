from django.contrib import admin
from basic.groups.models import *


class GroupMemberInline(admin.TabularInline):
    raw_id_fields = ('user',)
    model = GroupMember
    fk = 'group'

class GroupMessageInline(admin.TabularInline):
    raw_id_fields = ('user',)
    model = GroupMessage
    fk = 'topic'

class GroupPageInline(admin.TabularInline):
    model = GroupPage
    fk = 'group'


class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('creator',)
    inlines = (
        GroupPageInline,
        GroupMemberInline
    )
admin.site.register(Group, GroupAdmin)


class GroupTopicAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'group')
    inlines = (GroupMessageInline,)
admin.site.register(GroupTopic, GroupTopicAdmin)


class GroupMemberAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', 'group')
    list_display = ('user', 'group', 'status', 'created')
admin.site.register(GroupMember, GroupMemberAdmin)