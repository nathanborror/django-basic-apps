from django.conf.urls.defaults import *


urlpatterns = patterns('basic.relationships.views',
    url(r'^follow/(?P<to_user_id>\d+)/$',
        view='follow',
        name='relationship_follow'
    ),
    url(r'^unfollow/(?P<to_user_id>\d+)/$',
        view='unfollow',
        name='relationship_unfollow'
    ),
)