from django.template import Library
from django.template.defaultfilters import lower

register = Library()

@register.filter
def is_content_type(obj, arg):
    try:
        ct = lower(obj._meta.object_name)
        return ct == arg
    except AttributeError:
        return ""

@register.filter
def round(obj):
    "Returns a number rounded."
    try:
        return round(obj)
    except (ValueError,TypeError):
        return ""


@register.filter
def is_string(obj):
    return isinstance(obj, str)


@register.filter
def is_number(obj):
    return isinstance(obj, int)


@register.filter
def get_vars(obj):
    getvars = obj.copy()
    if 'page' in obj:
        del getvars['page']
    if len(getvars.keys()) > 0:
        return "&%s" % getvars.urlencode()
    else:
        return ''