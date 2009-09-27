from django.conf.urls.defaults import *
from basic.media.models import *


video_list = {
    'queryset': Video.objects.all(),
}
video_set_list = {
    'queryset': VideoSet.objects.all(),
}


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^sets/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=video_set_list,
        name='video_set_detail',
    ),
    url(r'^sets/$',
        view='object_list',
        kwargs=video_set_list,
        name='video_set_list',
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=video_list,
        name='video_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=video_list,
        name='video_list',
    ),
)