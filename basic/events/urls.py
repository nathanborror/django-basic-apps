from django.conf.urls.defaults import *


urlpatterns = patterns('basic.events.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/(?P<event_id>\d)/$',
        view='event_detail',
        name='event_detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        view='event_archive_day',
        name='event_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        view='event_archive_month',
        name='event_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        view='event_archive_year',
        name='event_archive_year'
    ),
    url(r'^$',
        view='event_list',
        name='event_index'
    ),
)