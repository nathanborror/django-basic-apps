from django.contrib import admin
from basic.elsewhere.models import *


class SocialNetworkProfileAdmin(admin.ModelAdmin):

    list_display = ('name', 'url', 'sort_order', )
    list_editable = ('sort_order',)

admin.site.register(Category)
admin.site.register(SocialNetworkProfile, SocialNetworkProfileAdmin)