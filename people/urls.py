from django.conf.urls.defaults import *
from basic.people import views as people_views


urlpatterns = patterns('',
  url(r'^types/(?P<slug>[-\w]+)/$',
    view=people_views.person_type_detail,
    name='person_type_detail'),

  url (r'^types/$',
    view=people_views.person_type_list,
    name='person_type_list'),

  url(r'^(?P<slug>[-\w]+)/$',
    view=people_views.person_detail,
    name='person_detail'),

  url (r'^$',
    view=people_views.person_list,
    name='person_list'),

  url(r'^quotes/(?P<slug>[-\w]+)/$',
    view=people_views.person_quote_list,
    name='person_quote_list'),
)
