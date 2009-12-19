from django import template
from django.contrib.contenttypes.models import ContentType
from basic.tools.templatetags.utils import parse_ttag

register = template.Library()


class GetFlagTypeNode(template.Node):
    def __init__(self, object_name, varname):
        self.object_name = object_name
        self.varname = varname

    def render(self, context):
        obj = template.resolve_variable(self.object_name, context)
        content_type = ContentType.objects.get_for_model(obj)
        flag_type_list = FlagType.objects.filter(content_type=content_type)
        context[self.varname] = flag_type_list
        return ''


@register.tag('get_flag_types')
def do_get_flag_types(parser, token):
    """
    Return flagging types for an object

    Syntax:

        {% get_flag_types for [object] as [varname] %}

    Usage:

        {% get_flag_types for entry as flag_type_list %}

    """
    tags = parse_ttag(token, ['for', 'as'])
    if len(tags) != 3:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return GetFlagTypeNode(object_name=tags['for'], varname=tags['as'])