from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^edit/$',
        view    = 'basic.profiles.views.profile_edit',
        name    = 'profile_edit',
    ),
    url(r'^(?P<username>[-\w]+)/$',
        view    = 'basic.profiles.views.profile_detail',
        name    = 'profile_detail',
    ),
    url (r'^$',
        view    = 'basic.profiles.views.profile_list',
        name    = 'profile_list',
    ),
)