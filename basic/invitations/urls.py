from django.conf.urls.defaults import *


urlpatterns = patterns('basic.invitations.views',
    url(r'^send/$',
        view='invitation_create',
        name='create'),

    url(r'^(?P<token>\w+)/$',
        view='invitation_detail',
        name='invitation'),
)