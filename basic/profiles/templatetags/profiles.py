import re

from django import template
from django.db import models
from django.utils.safestring import mark_safe

Profile = models.get_model('profiles', 'profile')

register = template.Library()


class GetProfiles(template.Node):
    def __init__(self, var_name, limit=None):
        self.var_name = var_name
        self.limit = limit

    def render(self, context):
        if self.limit:
            profiles = Profile.objects.select_related()[:int(self.limit)]
        else:
            profiles = Profile.objects.all()

        context[self.var_name] = profiles
        return ''


@register.tag
def get_profiles(parser, token):
    """
    Gets any number of latest posts and stores them in a varable.

    Syntax::

        {% get_profiles [limit] as [var_name] %}

    Example usage::

        {% get_profiles 10 as profile_list %}

        {% get_profiles as profile_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m1 = re.search(r'as (\w+)', arg)
    m2 = re.search(r'(.*?) as (\w+)', arg)

    if not m1:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    else:
        var_name = m1.groups()[0]
        return GetProfiles(var_name)

    if not m2:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    else:
        format_string, var_name = m2.groups()
        return GetProfiles(var_name, format_string[0])