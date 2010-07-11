from django.conf.urls.defaults import *
from django.contrib.comments.urls import urlpatterns


urlpatterns += patterns('basic.comments.views',
    url(r'^(?P<object_id>\d+)/edit/$',
        view='comment_edit',
        name='comments-edit'),

    url(r'^(?P<object_id>\d+)/remove/$',
        view='comment_remove',
        name='comments-remove'),
)
