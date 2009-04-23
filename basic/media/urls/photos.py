from django.conf.urls.defaults import *
from basic.media.models import *


photo_list = {
  'queryset': Photo.objects.all(),
}
photo_set_list = {
  'queryset': PhotoSet.objects.all(),
}


urlpatterns = patterns('',
  url(
    regex   = '^sets/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = photo_set_list,
    name    = 'photo_set_detail',
  ),
  url (
    regex   = '^sets/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = photo_set_list,
    name    = 'photo_set_list',
  ),
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = photo_list,
    name    = 'photo_detail',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = photo_list,
    name    = 'photo_list',
  ),
)