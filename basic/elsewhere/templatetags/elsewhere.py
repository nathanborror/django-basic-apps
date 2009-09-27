from django import template
from django.conf import settings
from django.db import models

from basic.elsewhere.models import SocialNetworkProfile

import re

register = template.Library()

class ElsewhereProfiles(template.Node):
    def __init__(self, var_name):
        self.var_name = var_name

    def render(self, context):
        profiles = SocialNetworkProfile.objects.all()
        context[self.var_name] = profiles
        return ''
        
@register.tag
def get_elsewhere_profiles(parser, token):
    """
    Gets elsewhere profile list.

    Syntax::

        {% get_elsewhere_profiles as [var_name] %}

    Example usage::

        {% get_elsewhere_profiles as elsewhere_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    var_name = m.groups()[0]
    return ElsewhereProfiles(var_name)