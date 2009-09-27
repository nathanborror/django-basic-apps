from django.views.generic import list_detail
from basic.music.models import *


def genre_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset=Genre.objects.all(),
    slug=slug,
  )
genre_detail.__doc__ = list_detail.object_detail.__doc__


def genre_list(request):
  return list_detail.object_list(
    request,
    queryset=Genre.objects.all(),
    paginate_by=20,
  )
genre_list.__doc__ = list_detail.object_list.__doc__


def label_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset=Label.objects.all(),
    slug=slug,
  )
label_detail.__doc__ = list_detail.object_detail.__doc__


def label_list(request):
  return list_detail.object_list(
    request,
    queryset=Label.objects.all(),
    paginate_by=20,
  )
label_list.__doc__ = list_detail.object_list.__doc__


def band_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset=Band.objects.all(),
    slug=slug,
  )
band_detail.__doc__ = list_detail.object_detail.__doc__


def band_list(request):
  return list_detail.object_list(
    request,
    queryset=Band.objects.all(),
    paginate_by=20,
  )
band_list.__doc__ = list_detail.object_list.__doc__


def album_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset=Album.objects.all(),
    slug=slug,
  )
album_detail.__doc__ = list_detail.object_detail.__doc__


def album_list(request):
  return list_detail.object_list(
    request,
    queryset=Album.objects.all(),
    paginate_by=20,
  )
album_list.__doc__ = list_detail.object_list.__doc__


def track_detail(request, slug):
  return list_detail.object_detail(
    request,
    queryset=Track.objects.all(),
    slug=slug,
  )
track_detail.__doc__ = list_detail.object_detail.__doc__


def track_list(request):
  return list_detail.object_list(
    request,
    queryset=Track.objects.all(),
    paginate_by=20,
  )
track_list.__doc__ = list_detail.object_list.__doc__