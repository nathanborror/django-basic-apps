from django.conf.urls.defaults import *
from basic.relationships import views as relationship_views


urlpatterns = patterns('',
    url(r'^follow/(?P<to_user_id>\d+)/$',
        view=relationship_views.follow,
        name='relationship_follow'),

    url(r'^stop-following/(?P<to_user_id>\d+)/$',
        view=relationship_views.stop_follow,
        name='relationship_stop_follow'),
)