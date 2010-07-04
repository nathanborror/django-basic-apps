from django.conf.urls.defaults import *


GROUP_URL = r'(?P<slug>[-\w]+)/'
PAGE_URL = r'%spages/(?P<page_slug>[-\w]+)/' % GROUP_URL
TOPIC_URL = r'%stopics/(?P<topic_id>\d+)/' % GROUP_URL
MESSAGE_URL = r'%smessages/(?P<message_id>\d+)/' % TOPIC_URL


urlpatterns = patterns('basic.groups.views.groups',
    url(r'^create/$',                           'group_create',         name='create'),
    url(r'^%s$' % GROUP_URL,                    'group_detail',         name='group'),
    url(r'^%sedit/$' % GROUP_URL,               'group_edit',           name='edit'),
    url(r'^%sremove/$' % GROUP_URL,             'group_remove',         name='remove'),
    url(r'^%sjoin/$' % GROUP_URL,               'group_join',           name='join'),
    url(r'^%smembers/$' % GROUP_URL,            'group_members',        name='members'),
    url(r'^%sinvite/$' % GROUP_URL,             'group_invite',         name='invite'),
    url(r'^$',                                  'group_list',           name='groups'),
)

# Topics
urlpatterns += patterns('basic.groups.views.topics',
    url(r'^%stopics/create/$' % GROUP_URL,      'topic_create',         name='topic_create'),
    url(r'^%s$' % TOPIC_URL,                    'topic_detail',         name='topic'),
    url(r'^%sedit/$' % TOPIC_URL,               'topic_edit',           name='topic_edit'),
    url(r'^%sremove/$' % TOPIC_URL,             'topic_remove',         name='topic_remove'),
    url(r'^%stopics/$' % GROUP_URL,             'topic_list',           name='topics'),
)

# Pages
urlpatterns += patterns('basic.groups.views.pages',
    url(r'^%spage/create/$' % GROUP_URL,        'page_create',          name='page_create'),
    url(r'^%s$' % PAGE_URL,                     'page_detail',          name='page'),
    url(r'^%sedit/$' % PAGE_URL,                'page_edit',            name='page_edit'),
    url(r'^%sremove/$' % PAGE_URL,              'page_remove',          name='page_remove'),
    url(r'^%spages/$' % GROUP_URL,              'page_list',            name='pages'),
)

# Messages
urlpatterns += patterns('basic.groups.views.messages',
    url(r'^%smessages/create/$' % TOPIC_URL,    'message_create',       name='message_create'),
    url(r'^%s$' % MESSAGE_URL,                  'message_detail',       name='message'),
    url(r'^%sedit/$' % MESSAGE_URL,             'message_edit',         name='message_edit'),
    url(r'^%sremove/$' % MESSAGE_URL,           'message_remove',       name='message_remove'),
    url(r'^%smessages/$' % TOPIC_URL,           'message_list',         name='messages'),
)
