from django.contrib import admin
from basic.people.models import *


class PersonTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(PersonType, PersonTypeAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_filter = ('person_types',)
    search_fields = ('first_name', 'last_name')
    prepopulated_fields = {'slug': ('first_name','last_name')}
admin.site.register(Person, PersonAdmin)


class QuoteAdmin(admin.ModelAdmin):
    list_display = ('person','quote')
    list_filter = ('person',)
    search_fields = ('quote',)
admin.site.register(Quote, QuoteAdmin)


class ConversationItemInline(admin.StackedInline):
    model = ConversationItem
    fk = 'conversation'


class ConversationAdmin(admin.ModelAdmin):
    inlines = [
        ConversationItemInline
    ]
admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationItem)