from django.conf.urls import *


USERNAME = r'(?P<username>[-.\w]+)'

urlpatterns = patterns('basic.relationships.views',
    url(r'^following/%s/$' % USERNAME,
        view='following',
        name='relationship_following'
    ),
    url(r'^followers/%s/$' % USERNAME,
        view='followers',
        name='relationship_followers'
    ),
    url(r'^follow/%s/$' % USERNAME,
        view='follow',
        name='relationship_follow'
    ),
    url(r'^unfollow/%s/$' % USERNAME,
        view='unfollow',
        name='relationship_unfollow'
    ),
    url(r'^block/%s/$' % USERNAME,
        view='block',
        name='relationship_block'
    ),
    url(r'^unblock/%s/$' % USERNAME,
        view='unblock',
        name='relationship_unblock'
    ),
)
