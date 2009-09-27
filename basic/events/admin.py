from django.contrib import admin
from basic.events.models import *


class EventTimeInline(admin.StackedInline):
    model = EventTime
    fk = 'event'


class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'place', 'created')
    inlines = [
        EventTimeInline
    ]
admin.site.register(Event, EventAdmin)