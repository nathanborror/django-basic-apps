from django.conf.urls.defaults import *


urlpatterns = patterns('basic.flagging.views',
    url(r'^flag/(?P<flag_type_slug>[-\w]+)/(?P<object_id>\d+)/$',
        view='flag',
        name='flag'
    ),
    url(r'^unflag/(?P<flag_type_slug>[-\w]+)/(?P<object_id>\d+)/$',
        view='unflag',
        name='unflag'
    ),
)