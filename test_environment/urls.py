from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^blog/', include('basic.blog.urls')),
    url(r'^bookmarks/', include('basic.bookmarks.urls')),
    url(r'^books/', include('basic.books.urls')),
    url(r'^comments/', include('basic.comments.urls')),
    url(r'^events/', include('basic.events.urls')),
    url(r'^flagging/', include('basic.flagging.urls')),
    url(r'^groups/', include('basic.groups.urls')),
    url(r'^invitations/', include('basic.invitations.urls')),
    url(r'^photos/', include('basic.media.urls.photos')),
    url(r'^movies/', include('basic.movies.urls')),
    url(r'^music/', include('basic.music.urls')),
    url(r'^people/', include('basic.people.urls')),
    url(r'^places/', include('basic.places.urls')),
    url(r'^profiles/', include('basic.profiles.urls')),
    url(r'^relationships/', include('basic.relationships.urls')),

    # Examples:
    # url(r'^$', '{{ project_name }}.views.home', name='home'),
    # url(r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views',
        (r'^media/(?P<path>.*)$', 'static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
