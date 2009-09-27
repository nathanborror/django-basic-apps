from django.shortcuts import get_object_or_404
from django.views.generic import list_detail
from basic.people.models import *


def person_type_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=PersonType.objects.all(),
        slug=slug,
        **kwargs
    )
person_type_detail.__doc__ = list_detail.object_detail.__doc__


def person_type_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=PersonType.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )
person_type_list.__doc__ = list_detail.object_list.__doc__


def person_detail(request, slug, **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Person.objects.all(),
        slug=slug,
        **kwargs
    )
person_detail.__doc__ = list_detail.object_detail.__doc__


def person_list(request, paginate_by=20, **kwargs):
    return list_detail.object_list(
        request,
        queryset=Person.objects.all(),
        paginate_by=paginate_by,
        **kwargs
    )
person_list.__doc__ = list_detail.object_list.__doc__


def person_quote_list(request, slug, template_name='people/person_quote_list.html', paginate_by=20, **kwargs):
    person = get_object_or_404(Person, slug__iexact=slug)
    return list_detail.object_list(
        request,
        queryset=person.quote_set.all(),
        paginate_by=paginate_by,
        template_name=template_name,
        extra_context={'person': person},
        **kwargs
    )
person_quote_list.__doc__ = list_detail.object_list.__doc__


def quote_detail(request, quote_id, template_name='people/quote_detail.html', **kwargs):
    return list_detail.object_detail(
        request,
        queryset=Quote.objects.all(),
        object_id=quote_id,
        **kwargs
    )
quote_detail.__doc__ = list_detail.object_detail.__doc__