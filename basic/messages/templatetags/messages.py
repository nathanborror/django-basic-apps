from django import template
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

from basic.tools.templatetags.utils import parse_ttag
from basic.tools.baseconv import base62

Message = models.get_model('messages', 'message')
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


class GetMessages(template.Node):
    def __init__(self, object_name, varname):
        self.object_name = object_name
        self.varname = varname

    def render(self, context):
        obj = template.resolve_variable(self.object_name, context)
        ctype = ContentType.objects.get_for_model(obj)
        message_list = Message.objects.filter(object_id=obj.id, content_type=ctype).order_by('id')
        context[self.varname] = message_list
        return ''

def do_get_messages(parser, token):
    """
    Get messages for an object.

    Syntax:
        {% get_messages for [object] as [varname] %}

    Example:
        {% get_messages for object as message_list %}
    """
    tags = parse_ttag(token, ['for', 'as'])
    if len(tags) != 3:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return GetMessages(object_name=tags['for'], varname=tags['as'])

register.tag('get_messages', do_get_messages)