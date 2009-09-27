import re

from django import template
from django.db import models
from django.utils.safestring import mark_safe

Person = models.get_model('people', 'person')

register = template.Library()


class GetPeople(template.Node):
    def __init__(self, var_name, limit=None):
        self.var_name = var_name
        self.limit = limit

    def render(self, context):
        if self.limit:
            people = Person.objects.select_related()[:int(self.limit)]
        else:
            people = Person.objects.all()

        context[self.var_name] = people
        return ''

@register.tag
def get_people(parser, token):
    """
    Gets any number of latest posts and stores them in a varable.

    Syntax::

        {% get_people [limit] as [var_name] %}

    Example usage::

        {% get_people 10 as people_list %}

        {% get_people as people_list %}
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
        return GetPeople(var_name)

    if not m2:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    else:
        format_string, var_name = m2.groups()
        return GetPeople(var_name, format_string[0])