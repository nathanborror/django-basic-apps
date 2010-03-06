from django.conf.urls.defaults import *


urlpatterns = patterns('basic.groups.views',
    # Groups
    url(r'^create/$',
        view='group_create',
        name='group_create'),

    url(r'^(?P<slug>[-\w]+)/$',
        view='group_detail',
        name='group'),

    url(r'^(?P<slug>[-\w]+)/page/create/$',
        view='group_page',
        name='group_page_create'),

    url(r'^(?P<slug>[-\w]+)/page/(?P<page_slug>[-\w]+)/$',
        view='group_page',
        name='group_page'),

    url(r'^(?P<slug>[-\w]+)/page/(?P<page_slug>[-\w]+)/edit/$',
        view='group_page_edit',
        name='group_page_edit'),

    url(r'^(?P<slug>[-\w]+)/page/(?P<page_slug>[-\w]+)/remove/$',
        view='group_page_remove',
        name='group_page_remove'),

    url(r'^(?P<slug>[-\w]+)/join/$',
        view='group_join',
        name='group_join'),

    url(r'^(?P<slug>[-\w]+)/remove/$',
        view='group_remove',
        name='group_remove'),

    url(r'^(?P<slug>[-\w]+)/edit/$',
        view='group_edit',
        name='group_edit'),

    url(r'^(?P<slug>[-\w]+)/members/$',
        view='group_members',
        name='group_members'),

    url(r'^(?P<slug>[-\w]+)/invite/$',
        view='group_invite',
        name='group_invite'),

    # Topics
    url(r'^(?P<slug>[-\w]+)/topics/create/$',
        view='topic_create',
        name='group_topic_create'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/messages/create/$',
        view='message_create',
        name='group_message_create'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/messages/(?P<message_id>\d+)/$',
        view='message_detail',
        name='group_topic_message'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/remove/$',
        view='topic_remove',
        name='group_topic_remove'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/edit/$',
        view='topic_edit',
        name='group_topic_edit'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/moderate/$',
        view='topic_moderate',
        name='group_topic_moderate'),

    url(r'^(?P<slug>[-\w]+)/topics/(?P<topic_id>\d+)/$',
        view='topic_detail',
        name='group_topic'),

    url(r'^(?P<slug>[-\w]+)/topics/$',
        view='topic_list',
        name='group_topics'),

    # Messages
    url(r'^(?P<slug>[-\w]+)/messages/(?P<message_id>\d+)/remove/$',
        view='message_remove',
        name='group_message_remove'),

    url(r'^(?P<slug>[-\w]+)/messages/(?P<message_id>\d+)/edit/$',
        view='message_edit',
        name='group_message_edit'),

    url(r'^(?P<slug>[-\w]+)/messages/(?P<message_id>\d+)/moderate/$',
        view='message_moderate',
        name='group_message_moderate'),

    url(r'^$',
        view='group_list',
        name='groups'),
)