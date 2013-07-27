from django.conf.urls import *


urlpatterns = patterns('basic.flagging.views',
    url(r'^flag/(?P<slug>[-\w]+)/(?P<app_label>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/$',
        view='flag',
        name='flag'
    ),
    url(r'^unflag/(?P<slug>[-\w]+)/(?P<app_label>\w+)/(?P<model>\w+)/(?P<object_id>\d+)/$',
        view='unflag',
        name='unflag'
    ),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$',
        view='user_flags',
        name='user_flags'
    ),
)