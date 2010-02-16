from django.conf.urls.defaults import *


urlpatterns = patterns('basic.messages.views',
    url(r'(?P<mailbox>sent|inbox)/(?P<object_id>\d+)/$',
        view='message_detail',
        name='message'),

    url(r'(?P<mailbox>inbox|trash|sent)/$',
        view='message_list',
        name='messages'),

    url(r'compose(?:/(?P<username>\w+))?/$',
        view='message_create',
        name='message_create'),

    url(r'remove/$',
        view='message_remove',
        name='message_remove'),

    url(r'',
        view='message_list',
        name='messages'),
)