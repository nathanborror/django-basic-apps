from django.conf.urls.defaults import *
from basic.media.models import *


photo_list = {
    'queryset': Photo.objects.all(),
}
photo_set_list = {
    'queryset': PhotoSet.objects.all(),
}


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^sets/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=photo_set_list,
        name='photo_set_detail',
    ),
    url (r'^sets/$',
        view='object_list',
        kwargs=photo_set_list,
        name='photo_set_list',
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=photo_list,
        name='photo_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=photo_list,
        name='photo_list',
    ),
)