from django import template
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from basic.tools.templatetags.utils import parse_ttag

register = template.Library()


class RenderTemplateNode(template.Node):
    def __init__(self, object_name, template_dir):
        self.object_name = object_name
        self.template_dir = template_dir.rstrip('/').strip('"').strip("'")

    def render(self, context):
        try:
            obj = template.resolve_variable(self.object_name, context)
            template_name = '%s.%s.html' % (obj._meta.app_label, obj._meta.module_name)
            template_list = [
                '%s/%s' % (self.template_dir, template_name),
                '%s/default.html' % self.template_dir
            ]
            context['object'] = obj
            return render_to_string(template_list, context)
        except AttributeError:
            if (type(obj) in (int, unicode, str)):
                return obj
            return ''
        except template.VariableDoesNotExist:
            return ''


@register.tag()
def render_template(parser, token):
    """
    Returns the proper template based on the objects content_type. If an
    template doesn't exist it'll fallback to default.html.

    Syntax:

        {% render_template for [object] in [path to templates] %}

    Usage:

        {% render_template for entry in "includes/lists" %}
    """
    tags = parse_ttag(token, ['for', 'in'])
    if len(tags) != 3:
        raise template.TemplateSyntaxError, '%r tag has invalid arguments' % tags['tag_name']
    return RenderTemplateNode(object_name=tags['for'], template_dir=tags['in'])
