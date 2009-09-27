from django.conf.urls.defaults import *
from basic.books.models import *


genre_list = {
  'queryset': Genre.objects.all(),
}
publisher_list = {
  'queryset': Publisher.objects.all(),
}
book_list = {
  'queryset': Book.objects.all(),
}


urlpatterns = patterns('',
  url(
    regex   = '^genres/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = genre_list,
    name    = 'book_genre_detail',
  ),
  url (
    regex   = '^genres/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = genre_list,
    name    = 'book_genre_list',
  ),
  url(
    regex   = '^publishers/(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = publisher_list,
    name    = 'book_publisher_detail',
  ),
  url (
    regex   = '^publishers/$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = publisher_list,
    name    = 'book_publisher_list',
  ),
  url(
    regex   = '^(?P<slug>[-\w]+)/$',
    view    = 'django.views.generic.list_detail.object_detail',
    kwargs  = book_list,
    name    = 'book_detail',
  ),
  url (
    regex   = '^$',
    view    = 'django.views.generic.list_detail.object_list',
    kwargs  = book_list,
    name    = 'book_list',
  ),
)