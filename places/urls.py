from django.conf.urls.defaults import *
from basic.places import views as place_views


urlpatterns = patterns('',
    url(r'^cities/(?P<slug>[-\w]+)/$',
        view=place_views.city_detail,
        name='place_city_detail'),

    url(r'^cities/$',
        view=place_views.city_list,
        name='place_city_list'),

    url(r'^types/(?P<slug>[-\w]+)/$',
        view=place_views.place_type_detail,
        name='place_type_detail'),

    url(r'^types/$',
        view=place_views.place_type_list,
        name='place_type_list'),

    url(r'^(?P<slug>[-\w]+)/$',
        view=place_views.place_detail,
        name='place_detail'),

    url(r'^$',
        view=place_views.place_list,
        name='place_list'),
)