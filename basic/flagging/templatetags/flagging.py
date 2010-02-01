from django import template
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from basic.tools.templatetags.utils import parse_ttag

FlagType = models.get_model('flagging', 'flagtype')

register = template.Library()


class GetFlagUrl(template.Node):
    def __init__(self, flag_type, object_name, slug):
        self.object_name = object_name
        self.slug = slug
        self.flag_type = flag_type

    def render(self, context):
        obj = template.resolve_variable(self.object_name, context)
        slug = template.resolve_variable(self.slug, context)
        content_type = ContentType.objects.get_for_model(obj)
        return reverse(self.flag_type, kwargs={
            'slug': slug,
            'ctype_id': content_type.pk,
            'object_id': obj.pk
        })


@register.tag('flag_url')
def do_flag_url(parser, token):
    """
    Return URL for flagging an object.

    Syntax:
        {% flag_url for [object] and [slug] %}

    Usage:
        {% flag_url for entry and 'offensive' %}
    """
    tags = parse_ttag(token, ['for', 'and'])
    if len(tags) != 3:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return GetFlagUrl('flag', object_name=tags['for'], slug=tags['and'])


@register.tag('unflag_url')
def do_unflag_url(parser, token):
    """
    Return URL for unflagging an object.

    Syntax:
        {% unflag_url for [object] and [slug] %}

    Usage:
        {% unflag_url for entry and 'offensive' %}
    """
    tags = parse_ttag(token, ['for', 'and'])
    if len(tags) != 3:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return GetFlagUrl('unflag', object_name=tags['for'], slug=tags['and'])