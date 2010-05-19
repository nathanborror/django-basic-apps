from django.conf.urls.defaults import *


urlpatterns = patterns('basic.messages.views',
    url(r'(?P<mailbox>inbox|trash|sent)/$',
        view='message_list',
        name='messages'),

    url(r'compose(?:/to:(?P<username>\w+))?/$',
        view='message_create',
        name='create'),

    url(r'remove/(?P<object_id>\d+)/$',
        view='message_remove',
        name='remove'),

    url(r'(?P<object_id>\d+)/$',
        view='message_detail',
        name='message'),

    url(r'',
        view='message_list',
        name='messages'),
)