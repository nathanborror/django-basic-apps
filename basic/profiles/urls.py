from django.conf.urls import *


USERNAME = r'(?P<username>[-.\w]+)'

urlpatterns = patterns('basic.profiles.views',
    url(r'^edit/$',
        view='profile_edit',
        name='profile_edit',
    ),
    url(r'^%s/$' % USERNAME,
        view='profile_detail',
        name='profile_detail',
    ),
    url (r'^$',
        view='profile_list',
        name='profile_list',
    ),
)