from django.conf.urls import *


urlpatterns = patterns('basic.places.views',
    url(r'^cities/(?P<slug>[-\w]+)/$',
        view='city_detail',
        name='place_city_detail'
    ),
    url(r'^cities/$',
        view='city_list',
        name='place_city_list'
    ),
    url(r'^types/(?P<slug>[-\w]+)/$',
        view='place_type_detail',
        name='place_type_detail'
    ),
    url(r'^types/$',
        view='place_type_list',
        name='place_type_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='place_detail',
        name='place_detail'
    ),
    url(r'^$',
        view='place_list',
        name='place_list'
    ),
)