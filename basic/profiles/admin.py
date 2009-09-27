from django.contrib import admin
from basic.profiles.models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city')
admin.site.register(Profile, ProfileAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('profile', 'service')
    list_filter = ('profile', 'service')
admin.site.register(Service, ServiceAdmin)


admin.site.register(MobileProvider)
admin.site.register(ServiceType)
admin.site.register(Link)