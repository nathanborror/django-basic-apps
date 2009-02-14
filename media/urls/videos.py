from django.conf.urls.defaults import *
from basic.media.models import *


video_list = {
  'queryset': Video.objects.all(),
}
video_set_list = {
  'queryset': VideoSet.objects.all(),
}


urlpatterns = patterns('',
  url(
    regex   = '^sets/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = video_set_list,
    name    = 'video_set_detail',
  ),
  url (
    regex   = '^sets/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = video_set_list,
    name    = 'video_set_list',
  ),
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = video_list,
    name    = 'video_detail',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = video_list,
    name    = 'video_list',
  ),
)