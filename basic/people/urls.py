from django.conf.urls.defaults import *


urlpatterns = patterns('basic.people.views',
    url(r'^types/(?P<slug>[-\w]+)/$',
        view='person_type_detail',
        name='person_type_detail'
    ),
    url (r'^types/$',
        view='person_type_list',
        name='person_type_list'
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='person_detail',
        name='person_detail'
    ),
    url (r'^$',
        view='person_list',
        name='person_list'
    ),
    url(r'^quotes/(?P<slug>[-\w]+)/$',
        view='person_quote_list',
        name='person_quote_list'
    ),
    url(r'^quote/(?P<quote_id>\d+)/$',
        view='quote_detail',
        name='quote_detail'
    ),
)
