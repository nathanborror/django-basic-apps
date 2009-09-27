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


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^genres/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=genre_list,
        name='book_genre_detail',
    ),
    url (r'^genres/$',
        view='object_list',
        kwargs=genre_list,
        name='book_genre_list',
    ),
    url(r'^publishers/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=publisher_list,
        name='book_publisher_detail',
    ),
    url (r'^publishers/$',
        view='object_list',
        kwargs=publisher_list,
        name='book_publisher_list',
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=book_list,
        name='book_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=book_list,
        name='book_list',
    ),
)