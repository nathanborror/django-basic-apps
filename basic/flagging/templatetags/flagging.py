from django import template
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()


@register.filter
def flag_url(obj, slug):
    """
    Returns a URL used to flag an object. Convenience filter instead of
    having to build the URL using the url template tag.

    Example:

        {{ object|flag_url:"flag-type-slug" }}

    """
    content_type = ContentType.objects.get_for_model(obj)
    return reverse('flag', kwargs={
        'slug': slug,
        'app_label': content_type.app_label,
        'model': content_type.model,
        'object_id': obj.pk
    })


@register.filter
def unflag_url(obj, slug):
    """
    Returns a URL used to unflag an object. Convenience filter instead of
    having to build the URL using the url template tag.

    Example:

        {{ object|unflag_url:"flag-type-slug" }}

    """
    content_type = ContentType.objects.get_for_model(obj)
    return reverse('unflag', kwargs={
        'slug': slug,
        'app_label': content_type.app_label,
        'model': content_type.model,
        'object_id': obj.pk
    })
