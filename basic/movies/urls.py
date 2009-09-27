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


urlpatterns = patterns('django.views.generic.list_detail',
    url(r'^genres/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=genre_list,
        name='movie_genre_detail',
    ),
    url (r'^genres/$',
        view='object_list',
        kwargs=genre_list,
        name='movie_genre_list',
    ),
    url(r'^studios/(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=studio_list,
        name='movie_studio_detail',
    ),
    url (r'^studios/$',
        view='object_list',
        kwargs=studio_list,
        name='movie_studio_list',
    ),
    url(r'^(?P<slug>[-\w]+)/$',
        view='object_detail',
        kwargs=movie_list,
        name='movie_detail',
    ),
    url (r'^$',
        view='object_list',
        kwargs=movie_list,
        name='movie_list',
    ),
)