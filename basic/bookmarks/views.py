from django.views.generic import date_based, list_detail
from basic.bookmarks.models import *


def bookmark_list(request, page=0):
    return list_detail.object_list(
        request,
        queryset=Bookmark.objects.all(),
        paginate_by=20,
        page=page,
    )
bookmark_list.__doc__ = list_detail.object_list.__doc__


def bookmark_archive_year(request, year):
    return date_based.archive_year(
        request,
        year=year,
        date_field='created',
        queryset=Bookmark.objects.published(),
        make_object_list=True,
  )
bookmark_archive_year.__doc__ = date_based.archive_year.__doc__


def bookmark_archive_month(request, year, month):
    return date_based.archive_month(
        request,
        year=year,
        month=month,
        date_field='created',
        queryset=Bookmark.objects.published(),
    )
bookmark_archive_month.__doc__ = date_based.archive_month.__doc__


def bookmark_archive_day(request, year, month, day):
    return date_based.archive_day(
        request,
        year=year,
        month=month,
        day=day,
        date_field='created',
        queryset=Bookmark.objects.published(),
    )
bookmark_archive_day.__doc__ = date_based.archive_day.__doc__


def bookmark_detail(request, object_id, year, month, day):
    return date_based.object_detail(
        request,
        year=year,
        month=month,
        day=day,
        date_field='created',
        object_id=object_id,
        queryset=Bookmark.objects.published(),
    )
bookmark_detail.__doc__ = date_based.object_detail.__doc__