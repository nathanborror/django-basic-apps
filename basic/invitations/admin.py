from django.contrib import admin

from basic.invitations.models import Invitation, InvitationAllotment


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'email', 'name', 'status', 'created')
    list_filter = ('status',)
admin.site.register(Invitation, InvitationAdmin)


class InvitationAllotmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount')
admin.site.register(InvitationAllotment, InvitationAllotmentAdmin)
