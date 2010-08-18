from django import template
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

from basic.tools.templatetags.utils import parse_ttag

Flag = models.get_model('flagging', 'flag')
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


@register.filter
def flagged_with(obj, slug):
    """
    Returns true of false based on whether the object is flagged one or more
    times with a particular flag type.
    """
    content_type = ContentType.objects.get_for_model(obj)
    flags = Flag.objects.filter(
        flag_type__slug=slug,
        content_type=content_type,
        object_id=obj.pk
    )
    return flags.count() != 0


class GetFlags(template.Node):
    def __init__(self, object_name, user, slug, varname):
        self.object_name = object_name
        self.user = user
        self.slug = slug
        self.varname = varname

    def render(self, context):
        obj = template.resolve_variable(self.object_name, context)
        user = template.resolve_variable(self.user, context)
        slug = template.resolve_variable(self.slug, context)
        content_type = ContentType.objects.get_for_model(obj)
        try:
            flag = Flag.objects.get(flag_type__slug=slug, content_type=content_type, object_id=obj.id, user=user)
        except Flag.DoesNotExist:
            flag = None
        context[self.varname] = flag
        return ''

@register.tag('get_flags')
def do_get_flags(parser, token):
    """
    Get flags for an object.

    Syntax:
        {% get_flags for [object] by [user] type [type-slug] as [varname] %}

    Example:
        {% get_flags for object by user type "favorites" as flag %}
    """
    tags = parse_ttag(token, ['for', 'by', 'type', 'as'])
    if len(tags) != 5:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return GetFlags(object_name=tags['for'], user=tags['by'], slug=tags['type'], varname=tags['as'])
