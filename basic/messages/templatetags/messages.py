from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse

from basic.tools.baseconv import base62

register = template.Library()


@register.simple_tag
def message_url(obj):
    """
    Given an object, returns its "message to" URL.
    
    Example::
    
        {% message_url obj %}
        
    """
    try:
        content_type = ContentType.objects.get(app_label=obj._meta.app_label, model=obj._meta.module_name)
        return reverse('messages:create', kwargs={
                'content_type_id': base62.from_decimal(content_type.pk),
                'object_id': base62.from_decimal(obj.pk)
                })
    except AttributeError:
        return ''