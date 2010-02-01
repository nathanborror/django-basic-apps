from django.conf.urls.defaults import *


urlpatterns = patterns('basic.flagging.views',
    url(r'^flag/(?P<slug>[-\w]+)/(?P<ctype_id>\d+)/(?P<object_id>\d+)/$',
        view='flag',
        name='flag'
    ),
    url(r'^unflag/(?P<slug>[-\w]+)/(?P<ctype_id>\d+)/(?P<object_id>\d+)/$',
        view='unflag',
        name='unflag'
    ),
)