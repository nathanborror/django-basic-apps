from django.conf.urls.defaults import *


urlpatterns = patterns('basic.relationships.views',
    url(r'^following/(?P<username>\w+)/$',
        view='following',
        name='relationship_following'
    ),
    url(r'^followers/(?P<username>\w+)/$',
        view='followers',
        name='relationship_followers'
    ),
    url(r'^follow/(?P<username>\w+)/$',
        view='follow',
        name='relationship_follow'
    ),
    url(r'^unfollow/(?P<username>\w+)/$',
        view='unfollow',
        name='relationship_unfollow'
    ),
    url(r'^block/(?P<username>\w+)/$',
        view='block',
        name='relationship_block'
    ),
    url(r'^unblock/(?P<username>\w+)/$',
        view='unblock',
        name='relationship_unblock'
    ),
)