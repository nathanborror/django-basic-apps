from django.views.generic import list_detail
from basic.places.models import *


def city_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=City.objects.all(),
        slug=slug,
        **kwargs
    )
city_detail.__doc__ = list_detail.object_detail.__doc__


def city_list(request, **kwargs):
    return list_detail.object_list(
        request,
        queryset=City.objects.all(),
        paginate_by=20,
        **kwargs
    )
city_list.__doc__ = list_detail.object_list.__doc__


def place_type_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=PlaceType.objects.all(),
        slug=slug,
        **kwargs
    )
place_type_detail.__doc__ = list_detail.object_detail.__doc__


def place_type_list(request, **kwargs):
    return list_detail.object_list(
        request,
        queryset=PlaceType.objects.all(),
        paginate_by=20,
        **kwargs
    )
place_type_list.__doc__ = list_detail.object_list.__doc__


def place_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Place.objects.all(),
        slug=slug,
        **kwargs
    )
place_detail.__doc__ = list_detail.object_detail.__doc__


def place_list(request, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Place.objects.all(),
        paginate_by=20,
        **kwargs
    )
place_list.__doc__ = list_detail.object_list.__doc__