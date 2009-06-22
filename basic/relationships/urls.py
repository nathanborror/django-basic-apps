from django.conf.urls.defaults import *
from basic.relationships import views as relationship_views


urlpatterns = patterns('',
    url(r'^follow/(?P<to_user_id>\d+)/$',
        view=relationship_views.follow,
        name='relationship_follow'),

    url(r'^unfollow/(?P<to_user_id>\d+)/$',
        view=relationship_views.unfollow,
        name='relationship_unfollow'),
)