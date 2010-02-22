from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def flag_url(obj, slug):
    content_type = ContentType.objects.get_for_model(obj)
    return reverse('flag', kwargs={
        'slug': slug,
        'ctype_id': content_type.pk,
        'object_id': obj.pk
    })


@register.filter
def unflag_url(obj, slug):
    content_type = ContentType.objects.get_for_model(obj)
    return reverse('unflag', kwargs={
        'slug': slug,
        'ctype_id': content_type.pk,
        'object_id': obj.pk
    })