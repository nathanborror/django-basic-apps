import re, datetime

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from django.views.generic import date_based, list_detail
from basic.events.models import *


def event_list(request, page=0):
    return list_detail.object_list(
        request,
        queryset=EventTime.objects.all(),
        paginate_by=20,
        page=page,
    )
event_list.__doc__ = list_detail.object_list.__doc__


def event_archive_year(request, year):
    return date_based.archive_year(
        request,
        year=year,
        date_field='start',
        queryset=EventTime.objects.all(),
        make_object_list=True,
        allow_future=True,
    )
event_archive_year.__doc__ = date_based.archive_year.__doc__


def event_archive_month(request, year, month):
    return date_based.archive_month(
        request,
        year=year,
        month=month,
        date_field='start',
        queryset=EventTime.objects.all(),
        allow_future=True,
    )
event_archive_month.__doc__ = date_based.archive_month.__doc__


def event_archive_day(request, year, month, day):
    return date_based.archive_day(
        request,
        year=year,
        month=month,
        day=day,
        date_field='start',
        queryset=EventTime.objects.all(),
        allow_future=True,
    )
event_archive_day.__doc__ = date_based.archive_day.__doc__


def event_detail(request, slug, year, month, day, event_id):
    return date_based.object_detail(
        request,
        year=year,
        month=month,
        day=day,
        date_field='start',
        object_id=event_id,
        queryset=EventTime.objects.all(),
        allow_future=True,
    )
event_detail.__doc__ = date_based.object_detail.__doc__