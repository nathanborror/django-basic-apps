from django.conf.urls.defaults import *


urlpatterns = patterns('basic.invitations.views',
    url(r'^send/$',
        view='invitation_create',
        name='create'),
)