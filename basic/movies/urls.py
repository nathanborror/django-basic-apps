from django.conf.urls.defaults import *
from basic.movies.models import *


genre_list = {
  'queryset': Genre.objects.all(),
}
movie_list = {
  'queryset': Movie.objects.all(),
}
studio_list = {
  'queryset': Studio.objects.all(),
}


urlpatterns = patterns('',
  url(
    regex   = '^genres/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = genre_list,
    name    = 'movie_genre_detail',
  ),
  url (
    regex   = '^genres/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = genre_list,
    name    = 'movie_genre_list',
  ),
  url(
    regex   = '^studios/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = studio_list,
    name    = 'movie_studio_detail',
   ),
   url (
    regex   = '^studios/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = studio_list,
    name    = 'movie_studio_list',
   ),
   url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = movie_list,
    name    = 'movie_detail',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = movie_list,
    name    = 'movie_list',
  ),
)