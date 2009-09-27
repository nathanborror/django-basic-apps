import re

from django import template
from basic.events.models import Event, EventTime

register = template.Library()


class UpcomingEventsNode(template.Node):
    def __init__(self, var_name, limit=10):
        self.var_name = var_name
        self.limit = limit

    def render(self, context):
        context[self.var_name] = EventTime.objects.order_by('-start')[:self.limit]


@register.tag
def get_upcoming_events(parser, token):
    """
    Returns a node which alters the context to provide upcoming events
    The upcoming events are stored in the variable specified.

    Syntax:
        {% get_upcoming_events <limit> as <varname> %}

    Example:
        {% get_upcoming_events 10 as upcoming_events %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    matches = re.search(r'([0-9]+) as (\w+)', arg)
    if not matches:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    limit, var_name = matches.groups()
    return UpcomingEventsNode(var_name, limit)