from django.contrib import admin
from basic.blog.models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display  = ('title', 'publish', 'status')
    list_filter   = ('publish', 'categories', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
            (None, {
                'fields': ('title', 'slug', 'author', 'markup',
                        'body', 'tease', 'status', 'allow_comments',
                        'publish', 'categories', 'tags', )
            }),
            ('Converted markup', {
                'classes': ('collapse',),
                'fields': ('body_markup', 'tease_markup', ),
            }),

        )
    
class SettingsAdmin(admin.ModelAdmin):
    
    fieldsets = (
            (None, {
                'fields': ('site', 'author_name', 'copyright', 'about',
                        'rss_url', 'twitter_url', 'email_subscribe_url', 'page_size',
                        'ping_google',)
            }),
            ('Meta options', {
                'classes': ('collapse',),
                'fields': ('meta_keywords', 'meta_description', ),
            }),

        )

class BlogRollAdmin(admin.ModelAdmin):

    list_display = ('name', 'url', 'sort_order', )
    list_editable = ('sort_order',)

admin.site.register(Post, PostAdmin)
admin.site.register(Settings, SettingsAdmin)
admin.site.register(BlogRoll, BlogRollAdmin)